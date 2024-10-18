# Biblical-text-Fetcher
This is a hackathon project where the gloal is to be able to fetch specified biblical passages from ChatGPT or BibleGateway and download the result as a .txt file.

## Setup Tutorial
[![IMAGE ALT TEXT](http://img.youtube.com/vi/88Zg0OQ0gCc/0.jpg)](http://www.youtube.com/watch?v=88Zg0OQ0gCc "Setup Tutorial Video")

## Verse Input Specification
Verses can be specified in the following ways:

* Individual verse: 1
* Verse range: 1-5
* Cherry-picked verses: 1,2,3,4,5
* Whole chapter: NULL (leaving it empty)

## Adding OpenAI API Key To CLI
1) Create a .env file in the cli/fetcher folder
2) In the .env file add the following line: ```OPENAI_API_KEY="YOUR-API-KEY"```

## Adding OpenAI API Key to Web App Server
1) Create .env file in the demo/server folder
2) In the .env file add the following line: ```OPENAI_API_KEY="YOUR-API-KEY"```
   
## How to Download CLI
1) Open terminal
2) Change directory to cli
3) Run the following command: ```pip install -e .```

## CLI Options

- **`--method` / `-p`** (required):  
  Specify the method for fetching the Bible passage:
  - `BG` for BibleGateway.
  - `GPT` for ChatGPT.
  
  Example: `--method BG`

- **`--version` / `-v`** (required):  
  Bible version for BibleGateway fetch, e.g., `NIV`, `KJV`, etc. For ChatGPT, the version can be ignored or set as `N/A`.

  Example: `--version NIV`

- **`--book` / `-b`** (required):  
  The name of the Bible book, e.g., `Genesis`, `John`.

  Example: `--book Genesis`

- **`--chapter` / `-c`** (required):  
  Chapter number in the book.

  Example: `--chapter 1`

- **`--verses` / `-vs`** (optional):  
  Comma-separated verse numbers (e.g., `1,2,3`) or range of verses (e.g., `1-5`). If not provided, the entire chapter will be fetched.

  Example: `--verses 1-5`

- **`--file` / `-f`** (optional):  
  Path to an input file containing multiple passage requests, where each line follows the format:

## CLI Usage

The CLI has two distinct usages and acts similar to pip. You can either use the manual approach by entering values for method, version, book, chapter, verses, or you can download passages in bulk by providing a path to a .txt file that has each line in the following form METHOD VERSION BOOK CHAPTER VERSES. 

### Manual Example
```bible-fetcher --method BG --version NIV --book Genesis --chapter 1 --verses 4,5```

### File-based Example
```bible-fetcher --file ./passages.txt```

where passages.txt looks like the following

```
GPT KJV Matthew 1 1-5
BG NKJV Genesis 1 4,5
BG NIV Genesis 1
```

## How to Run Web App
1) Open terminal
2) Change directory to demo/frontend
3) Run the following command: ```npm install```
4) Run the following command: ```npm run dev```
5) Open a new terminal window
6) Change directory to demo/server
7) Run the following command: ```pip install -r requirements.txt```
8) Run the following command: ```python index.py```
