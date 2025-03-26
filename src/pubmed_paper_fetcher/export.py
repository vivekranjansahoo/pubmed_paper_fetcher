import csv
import json

def save_to_csv(papers, filename, debug=False):
    """
    Save paper details to a CSV file while ensuring only expected fields are included.
    
    Parameters:
        papers (list): List of dictionaries containing paper details.
        filename (str): Output filename for the CSV.
        debug (bool): If True, enables detailed logging.
    """

    if not papers:
        print("⚠️ No data to save.")
        return

    # Define the expected column headers
    fieldnames = ["PubmedID", "Title", "Publication Date", "Company Affiliations", 
                  "Non-academic Authors", "Corresponding Author Email"]

    # 🔹 Sanitize the data (remove unwanted fields before processing)
    sanitized_papers = [{key: paper.get(key, "N/A") for key in fieldnames} for paper in papers]

    # 🔹 Debug Logging (only if enabled)
    if debug:
        print("\n---------------------------------")
        print("🔍 Data Preview before writing to CSV:\n", json.dumps(sanitized_papers, indent=4))
        print("---------------------------------\n")

    try:
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sanitized_papers)  # 🔹 Efficiently write all rows at once

        print(f"✅ Successfully saved {len(papers)} papers to {filename}")

    except Exception as e:
        print(f"❌ ERROR: Failed to save file.\n🛑 Reason: {e}")
        print("---------------------------------")
