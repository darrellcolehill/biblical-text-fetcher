# Standard imports
from typing import List, Set, Tuple
import logging
import re
import urllib.parse

# Library imports
import requests
from bs4 import BeautifulSoup


def bible_gateway_fetch(version: str, book: str, chapter: str, verses: List[int] = None) -> str:
    chapterText = get_passage_content(f"{book} {chapter}", version)

    if(verses != None):
        selectedVerses = extract_verses(chapterText, verses)
        return selectedVerses
    else:
        allVerses = extract_verses(chapterText)
        return allVerses
    

def get_passage_content(verse_ref: str, version: str) -> str:

    # Encode the verse ref so we can pass it to gateway
    verse_ref_encoded = urllib.parse.quote(verse_ref)

    # Construct url
    url = f"https://www.biblegateway.com/passage/?search={verse_ref_encoded}&version={version}"

    # Send a GET request to the provided URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return f"Failed to retrieve content. Status code: {response.status_code}"
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the div with the specific class name
    passage_div = soup.find('div', class_='passage-content passage-class-0')
    
    if not passage_div:
        return "Div with the specified class not found."

    # Replace <sup class="versenum"> elements with "VERSENUM-\d"
    for sup in passage_div.find_all('sup', class_='versenum'):
        versenum_text = sup.get_text(strip=True)  # Get the number inside <sup>
        sup.replace_with(f" VERSENUM-{versenum_text} ") 

    # Remove all <sup> and similar elements that might contain footnotes/cross-references
    for sup in passage_div.find_all('sup'):
        sup.decompose()  # Removes the element from the parsed HTML tree

    for sup in passage_div.find_all('h3'):
        sup.decompose()  # Removes the element from the parsed HTML tree

    # Find and remove the footnotes div if it exists
    footnotes_div = soup.find('div', class_='footnotes')
    if footnotes_div:
        footnotes_div.decompose()  # Removes the footnotes section entirely

    chapter_span = soup.find('span', class_='chapternum')
    if chapter_span:
        chapter_span.replace_with(f" VERSENUM-1 ") 

    # Find and remove the footnotes div if it exists
    hiddenCrossRef_div = soup.find('div', class_='crossrefs hidden')
    if hiddenCrossRef_div:
        hiddenCrossRef_div.decompose()  # Removes the footnotes section entirely
    
    # Extract and return the plain text without the footnotes
    return passage_div.get_text()


#  just populate verses correctly if they give a verse range using a for-loop
def extract_verses(text, verse_list: List = None):
    # Create a regex pattern to match the verses
    pattern = r"VERSENUM-(\d+)\s(.+?)(?=\sVERSENUM-\d+|$)"
    
    # Find all the verses using the pattern
    verses = re.findall(pattern, text, re.DOTALL)
    
    # Create a dictionary to store the verse number and corresponding text
    verse_dict = {int(num): verse.strip() for num, verse in verses}

    # If verse_list is None, return all verses
    if verse_list is None or len(verse_list) == 0:
        return ' '.join(verse_dict.values())
    
    # Extract the verses based on the provided verse_list
    extracted_verses = [verse_dict[verse_num] for verse_num in verse_list if verse_num in verse_dict]
    
    return ' '.join(extracted_verses)

# yoinkedVerseText = bible_gateway_yoink("NKJV", "Genesis", "1", [30])
# print(yoinkedVerseText)