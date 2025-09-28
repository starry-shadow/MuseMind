from dotenv import load_dotenv
load_dotenv()
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

# Urania the astronomy and astrology muse
feelings = """Today I had so much work I feel anxious and overwhelmed with work and personal responsibilities. 
I have trouble sleeping and concentrating. I often feel like I'm not good enough and worry about the future."""
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"""
    You are a story teller studying astronomy and astrology, focused on helping people's mental health. 
    This person you are talking to has these feelings: {feelings}.
    Give the story behind a constellation that teaches a positive lesson that can help with these feelings.
    What positive associations does this contellation have in astrology that can be reassuring."""
)
print(response.text)