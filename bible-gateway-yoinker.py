# Standard imports
from typing import List, Set, Tuple
import logging
import re
import urllib.parse

# Library imports
import requests

def yoink(version: str, book: str, chapter: str, verses: List[int] = None) -> str:
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


# TODO: update this to just handle verses being a list of integers.
#  just populate verses correctly if they give a verse range using a for-loop
def extract_verses(text, verses = -1):
    # Split the text into individual verses
    verse_list = text.split('VERSE-')[1:]  # Ignore the first empty split
    verses_dict = {int(verse.split(' ', 1)[0]): verse.split(' ', 1)[1] for verse in verse_list}

    extracted_verses = []

    for verse in verses:
        if isinstance(verse, int):  # If a single verse is provided
            extracted_verses.append(verses_dict.get(verse, f"Verse {verse} not found."))
        elif isinstance(verse, tuple) and len(verse) == 2:  # If a range of verses is provided
            start, end = verse
            for v in range(start, end + 1):
                extracted_verses.append(verses_dict.get(v, f"Verse {v} not found."))

    combined_text = ' '.join(extracted_verses)
    return combined_text


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

    # TODO: figure out why this is not working. 
    verse_text = re.sub(r'\s+', ' ', verse_text)  # Replace multiple spaces with a single space
    verse_text = verse_text.strip()

    # All done.
    return verse_text


# print(extract_reference_text(download_reference_html()))
print(yoink("NKJV", "Genesis", "1", verses=[1, 3]))