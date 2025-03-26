from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

PUBMED_API_URL = os.getenv("PUBMED_API_URL")
DETAILS_URL = os.getenv("DETAILS_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not (PUBMED_API_URL and DETAILS_URL and OPENAI_API_KEY):
    raise ValueError("Missing API_KEY. Check your .env file.")
