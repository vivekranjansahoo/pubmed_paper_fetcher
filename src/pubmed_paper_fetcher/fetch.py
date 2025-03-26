import requests
import xml.etree.ElementTree as ET
import re
import argparse
from config import PUBMED_API_URL, DETAILS_URL

def fetch_pubmed_papers(query: str, max_results: int = 5, debug: bool = False):
    """Fetch PubMed papers and extract company affiliations."""

    if debug:
        print(f"🔍 Searching for PubMed papers with query: {query} (Max results: {max_results})")

    # Step 1: Search for PubMed IDs
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    try:
        response = requests.get(PUBMED_API_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch PubMed IDs.\n🛑 Reason: {e}")
        return []

    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
    if not paper_ids:
        print("⚠️ No papers found for the given query.")
        return []

    if debug:
        print(f"✅ Found {len(paper_ids)} paper IDs: {', '.join(paper_ids)}")

    # Step 2: Fetch Full Paper Details (XML)
    details_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }

    try:
        details_response = requests.get(DETAILS_URL, params=details_params)
        details_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch paper details.\n🛑 Reason: {e}")
        return []

    root = ET.fromstring(details_response.text)  # Parse XML
    extracted_papers = []

    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text or "No Title Available"

        # Extract full publication date (Year, Month, Day)
        pub_date = article.find(".//PubDate")
        pub_year = pub_date.findtext("Year", "").strip()
        pub_month = pub_date.findtext("Month", "").strip()
        pub_day = pub_date.findtext("Day", "").strip()

        # Format the date properly
        full_pub_date = "-".join(filter(None, [pub_year, pub_month, pub_day])) or "Unknown"

        company_affiliations = []
        non_academic_authors = []
        corresponding_email = "N/A"

        for author in article.findall(".//Author"):
            first_name = author.findtext("ForeName", "").strip()
            last_name = author.findtext("LastName", "").strip()
            name = f"{first_name} {last_name}".strip()

            affiliation = author.findtext(".//AffiliationInfo/Affiliation", "")

            if affiliation:
                lower_aff = affiliation.lower()

                # Identify company affiliations (ignore universities, hospitals, etc.)
                if any(keyword in lower_aff for keyword in ["pharma", "biotech", "inc", "ltd", "corp", "gmbh", "sa", "srl", "co", "company"]):
                    company_affiliations.append(affiliation)
                    non_academic_authors.append(name)  # Mark author as non-academic

                # Extract Email using regex
                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
                if email_match:
                    corresponding_email = email_match.group(0)

        # Add Extracted Data to List
        paper_data = {
            "PubmedID": paper_id,
            "Title": title,
            "Publication Date": full_pub_date,
            "Company Affiliations": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Non-academic Authors": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Corresponding Author Email": corresponding_email
        }
        extracted_papers.append(paper_data)

        if debug:
            print(f"\n📄 Extracted Paper: {paper_data}")

    return extracted_papers

