import argparse
import os
from fetcher.bible_gateway_fetcher import bible_gateway_fetch
from fetcher.gpt_fetcher import chatgpt_fetch


def parse_verses(verses_str: str):
    """
    Parse a verse string which can be in the form:
    - Single verse (e.g., "1")
    - Comma-separated list of verses (e.g., "1,2,3")
    - Range of verses (e.g., "1-5")
    - Combination of single and range (e.g., "1,2,5-7")
    
    Returns a list of verses in the order they are listed.
    """
    verse_list = []
    parts = verses_str.split(',')
    
    for part in parts:
        if '-' in part:  # Handle range
            start, end = map(int, part.split('-'))
            verse_list.extend(range(start, end + 1))  # Include the end in the range
        else:
            verse_list.append(int(part))  # Single verse
    
    return verse_list  # Keep the order and duplicates as listed


def parse_passage_line(line: str):
    """
    Parse a line of text in the format:
    "METHOD VERSION BOOK CHAPTER VERSES"
    Example: "BG NIV Genesis 1 1,2,3"
    """
    parts = line.strip().split()

    method_prefix = parts[0]  # "GPT" or "BG"
    version = parts[1]        # Bible version, e.g., "NIV"
    book = parts[2]           # Bible book, e.g., "Genesis"
    chapter = parts[3]        # Chapter number, e.g., "1"
    
    # Parse verses, if provided
    if len(parts) > 4:
        verses = parse_verses(parts[4])  # Verses in various formats
    else:
        verses = []  # Default to an empty list if no verses are provided

    return method_prefix, version, book, chapter, verses


def process_input_file(file_path: str):
    """
    Process the input file line by line and fetch Bible passages using the appropriate method.
    Each line should be in the format:
    "METHOD VERSION BOOK CHAPTER VERSES"
    """
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():  # Ignore empty lines
                method_prefix, version, book, chapter, verses = parse_passage_line(line)

                if method_prefix == "BG":
                    print(bible_gateway_fetch(version, book, chapter, verses))
                elif method_prefix == "GPT":
                    print(chatgpt_fetch(book, chapter, verses))
                else:
                    print(f"Unknown method prefix: {method_prefix}")


def process_manual_input(method_prefix: str, version: str, book: str, chapter: str, verses: str):
    verses = parse_verses(verses) if verses else []
    
    if method_prefix == "BG":
        bg_text = bible_gateway_fetch(version, book, chapter, verses)
        save_passage_to_file("BG", version, book, chapter, verses, bg_text)
    elif method_prefix == "GPT":
        gpt_text = chatgpt_fetch(version, book, chapter, verses)
        save_passage_to_file("GPT", version, book, chapter, verses, gpt_text)
    else:
        print(f"Unknown method prefix: {method_prefix}")


def save_passage_to_file(method, version, book, chapter, verses, passage_text):
    """Save the passage to a file in the current directory with a specific naming convention."""
    # Create the file name based on METHOD_VERSION_BOOK_CHAPTER_VERSES
    verses_part = f"_{','.join(map(str, verses))}" if verses else ""
    file_name = f"{method}_{version}_{book}_{chapter}{verses_part}.txt"
    
    # Ensure file name is valid for the filesystem (replace invalid characters like slashes)
    file_name = file_name.replace("/", "-")
    
    # Get the current directory where the CLI is being called
    current_directory = os.getcwd()
    
    # Create the full path to the file
    file_path = os.path.join(current_directory, file_name)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(passage_text)
        print(f"Passage saved successfully as {file_name}")
    except IOError as e:
        print(f"Error saving passage to file: {e}")


def entry_point():
    parser = argparse.ArgumentParser(description="Fetch Bible passages from ChatGPT or BibleGateway")
    
    # Allow input file as an optional argument
    parser.add_argument('--file', '-f', type=str, help="Path to input file containing multiple passage requests", required=False)
    
    # Manual input details
    parser.add_argument('--method', '-p', type=str, help="Method prefix: 'GPT' or 'BG'", required=True)
    parser.add_argument('--version', '-v', type=str, help="Bible version for BibleGateway fetch", required=True)
    parser.add_argument('--book', '-b', type=str, help="Book name (e.g., 'Genesis')", required=True)
    parser.add_argument('--chapter', '-c', type=str, help="Chapter number", required=True)
    parser.add_argument('--verses', '-vs', type=str, help="Comma-separated verse numbers (e.g., '1,2,3' or '1-5')", required=False)

    args = parser.parse_args()

    if args.file:
        # File-based input, process the entire file
        process_input_file(args.file)
    else:
        # Manual input: method, version, book, chapter, verses
        process_manual_input(args.method, args.version, args.book, args.chapter, args.verses or "")