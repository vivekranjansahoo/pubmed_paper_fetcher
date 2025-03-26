import argparse
import json
import time
from pubmed_paper_fetcher.fetch import fetch_pubmed_papers
from pubmed_paper_fetcher.process import extract_relevant_fields
from pubmed_paper_fetcher.filter import is_non_academic
from pubmed_paper_fetcher.export import save_to_csv

def main():
    """
    Entry point for fetching, processing, and saving PubMed research papers.
    Supports debugging and handles errors gracefully.
    """
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers.")
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-n", "--num_results", type=int, default=5, help="Number of results to fetch (default: 5)")
    parser.add_argument("-f", "--file", help="Output filename", default="output.csv")
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")

    args = parser.parse_args()

    print("\n================= PubMed Research Paper Fetcher =================")
    print(f"🔍 Searching for papers related to: **{args.query}**")
    print("------------------------------------------------------------------")

    if args.debug:
        print(f"🛠 Debug mode enabled. Output will be verbose.")
        print("------------------------------------------------------------------")

    try:
        # Introduce a short delay to prevent API rate limiting
        time.sleep(1)  

        print("📡 Fetching papers from PubMed API...")
        papers = fetch_pubmed_papers(args.query,args.num_results, args.debug)

        if not isinstance(papers, list):
            raise ValueError("Unexpected response format: Expected a list of papers.")

        print(f"✅ Successfully fetched {len(papers)} papers.")
        print("------------------------------------------------------------------")

        if args.debug:
            print(f"📜 Sample Output (First 2 papers):\n")
            debug_output = [
                {
                    "PubmedID": paper.get("PubmedID", "N/A"),
                    "Title": paper.get("Title", "N/A"),
                    "Publication Date": paper.get("Publication Date", "N/A"),
                    "Affiliations": paper.get("Company Affiliations", "N/A"),  # Field renamed
                    "Authors": paper.get("Non-academic Authors", "N/A"),  # Field renamed
                    "Corresponding Author Email": paper.get("Corresponding Author Email", "N/A"),
                }
                for paper in papers[:2]  # Show only first 2 papers for debugging
            ]
            print(json.dumps(debug_output, indent=2))
            print("------------------------------------------------------------------")

    except Exception as e:
        print("❌ ERROR: Failed to fetch papers.")
        print(f"   🛑 Reason: {e}")
        print("------------------------------------------------------------------")
        return

    processed_papers = []

    print("📝 Processing fetched papers...")
    print("------------------------------------------------------------------")

    for paper in papers:
        try:
            extracted = extract_relevant_fields(paper)

            authors = paper.get("Authors", [])
            affiliations = paper.get("Affiliations", [])

            print("🔍 LLM is searching and filtering based on data...")

            # Identify non-academic authors based on affiliations
            extracted["Authors"] = [
                author for author, aff in zip(authors, affiliations) if is_non_academic(aff)
            ] if authors and affiliations else "N/A"

            processed_papers.append(extracted)

            print("✅ Classification completed successfully!")

        except Exception as e:
            print(f"⚠️ Skipping a paper due to processing error: {e}")
            print("------------------------------------------------------------------")

    print(f"✅ Processing complete. {len(processed_papers)} papers processed successfully.")
    print("------------------------------------------------------------------")

    # Save processed data to CSV
    try:
        print(f"💾 Saving papers to file: {args.file} ...")
        save_to_csv(processed_papers, args.file,args.debug)
        print("==================================================================\n")

    except Exception as e:
        print("❌ ERROR: Failed to save file.")
        print(f"   🛑 Reason: {e}")
        print("------------------------------------------------------------------")

if __name__ == "__main__":
    main()
