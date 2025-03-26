import os
import pytest
from dotenv import load_dotenv

# Load .env variables for testing
load_dotenv()

# Test if all environment variables are correctly loaded
def test_env_variables_exist():
    assert os.getenv("PUBMED_API_URL") is not None, "PUBMED_API_URL is missing"
    assert os.getenv("DETAILS_URL") is not None, "DETAILS_URL is missing"
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is missing"


