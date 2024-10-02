import os
from dotenv import load_dotenv
import openai

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if not key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = key

client = openai.OpenAI()

def chatgpt_yoink(version, book, chapter, verses, model="gpt-3.5-turbo"):
    if verses is not None and len(verses) > 0:
        verseString = ', '.join(map(str, verses))
        prompt = f"Get {book} {chapter}:{verseString} from the {version}. Give me only the plain-text with no verse markers and no chapter markers"
    else:
        prompt = f"Get {book} {chapter} from the {version}. Give me only the plain-text with no verse markers and no chapter markers"

    try:
        # Call OpenAI's ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {e}"

# if __name__ == "__main__":
#     response = chatgpt_yoink("NKJV", "Genesis", "1", [1, 2, 3, 4, 5])
#     print("ChatGPT Response:")
#     print(response)
