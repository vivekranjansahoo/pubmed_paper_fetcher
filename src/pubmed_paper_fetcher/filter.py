import openai
import time
from config import OPENAI_API_KEY

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Cache to store previously classified affiliations with timestamps
affiliation_cache = {}

# Cache expiry time in seconds (e.g., 24 hours)
CACHE_EXPIRY_TIME = 24 * 60 * 60  

def classify_affiliations(affiliations, force_refresh=True):
    """
    Classifies a list of affiliations as 'Academic' or 'Non-Academic' (e.g., biotech, pharma, corporations).

    Uses OpenAI's GPT model to perform batch classification, reducing API calls.
    Cached results are used unless they are outdated or force_refresh is enabled.

    Parameters:
        affiliations (list[str]): List of institution/organization names.
        force_refresh (bool): If True, forces reclassification even if cached.

    Returns:
        dict: Mapping of each affiliation to either 'Academic' or 'Non-Academic'.
    """
    if not affiliations:
        return {}

    current_time = time.time()

    # Remove duplicates & filter out expired or missing cache entries
    unique_affiliations = [
        aff for aff in set(affiliations)
        if force_refresh or aff not in affiliation_cache or (current_time - affiliation_cache[aff]["timestamp"]) > CACHE_EXPIRY_TIME
    ]

    # Return cached results if all affiliations have been classified before
    if not unique_affiliations:
        return {aff: affiliation_cache[aff]["category"] for aff in affiliations}

    # Construct a concise and structured prompt for classification
    prompt = (
        "Classify the following institutions as 'Academic' or 'Non-Academic' "
        "(e.g., biotech, pharma, corporation). Provide only 'Academic' or 'Non-Academic' "
        "for each entry, strictly without explanations.\n\n"
    )
    prompt += "\n".join(f"- {aff}" for aff in unique_affiliations)

    print("🔍 LLM is searching and filtering based on data...")

    try:
        # Call OpenAI GPT model for batch classification
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in classifying institutions."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract classification results from the API response
        results = response["choices"][0]["message"]["content"].strip().split("\n")

        # Map the results to their corresponding affiliations
        classification = {}
        for aff, result in zip(unique_affiliations, results):
            result = result.strip().lower()
            category = "Non-Academic" if result == "non-academic" else "Academic"

            classification[aff] = category
            affiliation_cache[aff] = {"category": category, "timestamp": current_time}  # Store in cache with timestamp

        print("✅ Classification completed successfully!")

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        # If API call fails, return 'Unknown' instead of losing data
        classification = {aff: "Unknown" for aff in unique_affiliations}  

    # Merge results with cached classifications and return final dictionary
    return {aff: affiliation_cache.get(aff, {}).get("category", "Unknown") for aff in affiliations}

def is_non_academic(affiliation: str, force_refresh=True) -> bool:
    """
    Determines if a given institution is 'Non-Academic'.

    Uses the batch classifier function internally, ensuring that cached results are utilized.

    Parameters:
        affiliation (str): The name of the institution to classify.
        force_refresh (bool): If True, forces reclassification even if cached.

    Returns:
        bool: True if the affiliation is classified as 'Non-Academic', otherwise False.
    """
    return classify_affiliations([affiliation], force_refresh).get(affiliation, "Academic") == "Non-Academic"
