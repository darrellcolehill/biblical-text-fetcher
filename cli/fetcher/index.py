import argparse
from fetcher.bible_gateway_fetcher import bible_gateway_fetch
from fetcher.gpt_fetcher import chatgpt_fetch



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
        verses = list(map(int, parts[4].split(',')))  # Verses as a list of integers
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
    verses = list(map(int, verses.split(','))) if verses else []
    
    if method_prefix == "BG":
        print(bible_gateway_fetch(version, book, chapter, verses))
    elif method_prefix == "GPT":
        print(chatgpt_fetch(book, chapter, verses))
    else:
        print(f"Unknown method prefix: {method_prefix}")


def entry_point():
    parser = argparse.ArgumentParser(description="Fetch Bible passages from ChatGPT or BibleGateway")
    
    # Allow input file as an optional argument
    parser.add_argument('--file', '-f', type=str, help="Path to input file containing multiple passage requests", required=False)
    
    # Manual input details
    parser.add_argument('--method', '-p', type=str, help="Method prefix: 'GPT' or 'BG'", required=True)
    parser.add_argument('--version', '-v', type=str, help="Bible version for BibleGateway fetch", required=True)
    parser.add_argument('--book', '-b', type=str, help="Book name (e.g., 'Genesis')", required=True)
    parser.add_argument('--chapter', '-c', type=str, help="Chapter number", required=True)
    parser.add_argument('--verses', '-vs', type=str, help="Comma-separated verse numbers (e.g., '1,2,3')", required=False)

    args = parser.parse_args()

    if args.file:
        # File-based input, process the entire file
        process_input_file(args.file)
    else:
        # Manual input: method, version, book, chapter, verses
        process_manual_input(args.method, args.version, args.book, args.chapter, args.verses or "")