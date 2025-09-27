from dotenv import load_dotenv
load_dotenv()
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

# Urania the astronomy and astrology muse
constellation=input("Enter a constellation:\n")
# print("constellation is "+constellation)
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"Give the story behind {constellation}. What lesson does that story teach?"
)
print(response.text)