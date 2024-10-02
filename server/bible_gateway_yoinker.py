# Standard imports
from typing import List, Set, Tuple
import logging
import re
import urllib.parse

# Library imports
import requests

def bible_gateway_yoink(version: str, book: str, chapter: str, verses: List[int] = None) -> str:
    html = download_reference_html(f"{book} {chapter}", version)
    chapterText = extract_reference_text(html)
    if(verses != None):
        return extract_verses(chapterText, verses)
    else:
        # TODO: verify that this is working 
        return extract_verses(chapterText)


def download_reference_html(verse_ref: str, version: str) -> str:
    """Pulls HTML from BibleGateway"""

    # Encode the verse ref so we can pass it to gateway
    verse_ref_encoded = urllib.parse.quote(verse_ref)

    # Construct url
    url = f"https://www.biblegateway.com/passage/?search={verse_ref_encoded}&version={version}"

    # Pull page from gateway
    response = requests.get(url, timeout=10)

    # Done.
    logging.debug(response.text)
    return response.text


#  just populate verses correctly if they give a verse range using a for-loop
def extract_verses(text, verse_list: List = None):
    # Create a regex pattern to match the verses
    pattern = r"VERSE-(\d+)\s(.+?)(?=\sVERSE-\d+|$)"
    
    # Find all the verses using the pattern
    verses = re.findall(pattern, text, re.DOTALL)
    
    # Create a dictionary to store the verse number and corresponding text
    verse_dict = {int(num): verse.strip() for num, verse in verses}

    # If verse_list is None, return all verses
    if verse_list is None:
        return ' '.join(verse_dict.values())
    
    # Extract the verses based on the provided verse_list
    extracted_verses = [verse_dict[verse_num] for verse_num in verse_list if verse_num in verse_dict]
    
    return ' '.join(extracted_verses)


def extract_reference_text(html: str) -> str:
    """Given HTML from BG, pull out just the Scripture text and keeps verse numbers."""

    # Use a regex pattern to find the correct content div
    match = re.search(
        r'<div class=\'passage-content passage-class-0.*?>(.*?)</div>',
        html,
        re.DOTALL
    )

    if not match:
        print(html)
        raise SyntaxError("Couldn't find verse content")

    # Get the verse text from the match
    verse_text = match.group(1).strip()

    # Remove <sup> tags with class 'chapternum' and replace with '1'
    verse_text = re.sub(r'<span[^>]*class=["\']chapternum["\'][^>]*>(.*?)</span>', 'VERSE-1 ', verse_text, flags=re.IGNORECASE)
    # Remove <sup> tags with class 'versenum' and keep the number inside
    verse_text = re.sub(r'<sup[^>]*class=["\']versenum["\'][^>]*>(.*?)</sup>', r'VERSE-\1', verse_text, flags=re.IGNORECASE)

    # Scrub metadata
    verse_text = re.sub(r"<sup (.*?)</sup>", "", verse_text)
    verse_text = re.sub(r'<div [^>]+>', '', verse_text)
    verse_text = re.sub(r'<h3>.*?</h3>', '', verse_text)
    verse_text = re.sub(r'<h4>.*?</h4>', '', verse_text)

    # Remove the ordered list <ol> and its content (footnotes)
    verse_text = re.sub(r'<ol>.*?</ol>', '', verse_text, flags=re.DOTALL)

    # Remove other unwanted tags
    verse_text = re.sub(r'<p[^>]*>', '', verse_text)
    verse_text = re.sub(r'</p>', ' ', verse_text)
    verse_text = re.sub(r'<span[^>]*>', ' ', verse_text)
    verse_text = re.sub(r'</span>', ' ', verse_text)
    verse_text = re.sub(r'<a[^>]*>', '', verse_text)
    verse_text = re.sub(r'</a>', '', verse_text)

    verse_text = re.sub(r'<i[^>]*>', '', verse_text)
    verse_text = re.sub(r'</i>', '', verse_text)

    verse_text = re.sub(r'<br[^>]*>', ' ', verse_text)
    verse_text = re.sub(r'&nbsp;', ' ', verse_text)

    # Clean up any remaining whitespace
    verse_text = re.sub(r'\s+', ' ', verse_text)  # Replace multiple spaces with a single space
    verse_text = verse_text.strip()

    # All done.
    return verse_text

# yoinkedVerseText = bible_gateway_yoink("NKJV", "Genesis", "1", [30])
# print(yoinkedVerseText)