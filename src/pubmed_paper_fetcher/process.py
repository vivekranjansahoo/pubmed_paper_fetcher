def extract_relevant_fields(paper_data):
    """
    Extracts key fields from PubMed paper data, including author affiliations, company associations, 
    and corresponding author email.

    The function identifies:
    - Company affiliations based on biotech/pharma-related keywords.
    - Non-academic authors who do not belong to academic institutions.
    - The corresponding author's email, if available.

    Parameters:
        paper_data (dict): A dictionary containing metadata about a PubMed paper.

    Returns:
        dict: A dictionary with extracted and categorized information:
            - PubmedID (str)
            - Title (str)
            - Publication Date (str)
            - Company Affiliations (str)
            - Non-academic Authors (str)
            - Corresponding Author Email (str)
    """

    # Extract list of authors from paper data; default to an empty list if missing
    authors = paper_data.get("authors", [])

    # Use sets to ensure unique values and avoid duplicate affiliations/authors
    non_academic_authors = set()
    company_affiliations = set()
    corresponding_author_email = "N/A"  # Default value if no email is found

    # Define keyword sets for classification
    academic_keywords = {"university", "institute", "college", "school", "academy", "research", "lab"}
    company_keywords = {"pharma", "biotech", "therapeutics", "biosciences", "lifesciences", "genomics", "biopharma"}

    for author in authors:
        if isinstance(author, dict):  # Ensure the author data is a dictionary before proceeding
            affiliation = author.get("affiliation", "").strip()
            email = author.get("email", "").strip()
            name = author.get("name", "Unknown Author").strip()

            # Normalize affiliation for case-insensitive keyword matching
            lower_affiliation = affiliation.lower()

            # Identify pharmaceutical/biotech company affiliations
            if any(word in lower_affiliation for word in company_keywords):
                company_affiliations.add(affiliation)

            # Classify non-academic authors (those not affiliated with academic institutions)
            if not any(word in lower_affiliation for word in academic_keywords):
                non_academic_authors.add(name)

            # Capture the first available corresponding author email
            if email and corresponding_author_email == "N/A":
                corresponding_author_email = email

    # Construct the final result dictionary
    return {
        "PubmedID": paper_data.get("PubmedID", "N/A"),  # Default to "N/A" if missing
        "Title": paper_data.get("Title", "No Title Available"),
        "Publication Date": paper_data.get("Publication Date", "Unknown Date"),
        "Company Affiliations": ", ".join(company_affiliations) if company_affiliations else "N/A",
        "Non-academic Authors": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
        "Corresponding Author Email": corresponding_author_email
    }
