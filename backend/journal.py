from dotenv import load_dotenv
load_dotenv()
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()


# Clio, the muse of history
journal_entry = """Today I had so much work I feel anxious and overwhelmed with work and personal responsibilities. 
I have trouble sleeping and concentrating. I often feel like I'm not good enough and worry about the future."""

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"""
    You are a therapist, focused on helping people's mental health. Looking at their journal.
    Help them to work through there feelings. (this is not a conversation though, its just feedback and advice)
    Do not ask questions to them, they cannot respond, but you can suggest things they can think about to self reflect,
    provide advice, provide understand empathy and reassurance. You also have a slight interest in history so
    consider using historical anecdotes to help. Here is their journal entry: 
    
    {journal_entry}."""
)
print(response.text)