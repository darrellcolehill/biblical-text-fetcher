import os
from dotenv import load_dotenv
import openai

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if not key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")


# Set the API key for OpenAI
openai.api_key = key

def chatgpt_yoink(version, book, chapter, verses, model="gpt-3.5-turbo"):


    verseString = ', '.join(map(str, verses))
    
    prompt = f"Get {book} {chapter}:{verseString} from the {version}. Give me only the plain-text with no verse markers and no chapter markers"
    try:
        # Call OpenAI's ChatGPT API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        # Return the content of the assistant's message
        return response.choices[0].message['content'].strip()

    except Exception as e:
        return f"Error: {e}"

# if __name__ == "__main__":
#     user_input = input("Enter your prompt: ")
#     response = call_chatgpt(user_input)
#     print("ChatGPT Response:")
#     print(response)
