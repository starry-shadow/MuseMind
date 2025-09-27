from dotenv import load_dotenv
load_dotenv()
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Give me the history of the Roman Empire"
)
print(response.text)