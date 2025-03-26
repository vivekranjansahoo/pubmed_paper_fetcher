# PubMed Paper Fetcher - Vivek

## 📌 Overview

**PubMed Paper Fetcher** is a Python package that helps fetch **PubMed research papers** with **pharmaceutical or biotech-affiliated authors** and exports the results as CSV. It automates the data retrieval process using the **PubMed API**, allowing researchers and developers to efficiently gather and analyze research papers.

---

## 🚀 Features

- Fetch **PubMed research papers** based on **specific criteria**.
- Extract **author affiliations** related to **pharmaceutical/biotech** industries.
- Export results to a **CSV file**.
- Supports **.env configuration** for API keys.
- CLI tool support for ease of use.

---

## 📁 Folder Structure

```
📦 pubmed-paper-fetcher-vivek
├── 📂 src
│   ├── 📂 pubmed_paper_fetcher
│   │   ├── __init__.py
│   │   ├── export.py # Exporting results to CSV
│   │   ├── fetch.py  # Main logic to fetch papers from PubMed API
│   │   ├── filter.py   # filtering logic
│   │   └── process.py  # Parsing the fetch papers
│   ├── 📂 cli
│   │   ├── __init__.py
│   │   └── main.py  # CLI interface
├── config.py  # Configuration settings
├── .env  # Environment variables (API keys, credentials, etc.)
├── pyproject.toml  # Poetry dependency manager file
├── README.md  # Documentation
└── tests  # Unit tests
```

---

## 🛠 Installation Guide

### 🔹 Prerequisites

Ensure you have:

- **Python 3.11+** installed
- **Poetry (Dependency Manager)** installed
- **API Key** for PubMed

### 🔹 Step 1: Clone the Repository

```sh
git clone https://github.com/vivekranjansahoo/pubmed_paper_fetcher.git
cd pubmed-paper-fetcher
```

### 🔹 Step 2: Install Dependencies

Using **Poetry**:

```sh
poetry install
```


### 🔹 Step 3: Configure Environment Variables

Create a **.env** file in the root directory:

```sh
touch .env
```

Add the following to **.env**:

```ini
PUBMED_API_URL="your_pubmed_api_url"
DETAILS_URL="your_pubmed_esummary_url"
OPENAI_API_KEY="your key"
```

### 🔹 Step 4: Run the CLI Tool

```sh
poetry run get-papers-list "COVID-19 Vaccine"
```


---

## ⚙️ Usage

Run the CLI tool:
```bash
poetry run get-papers-list "cancer treatment" -n 10 -f results.csv -d
```

### Arguments
| Argument | Description |
|----------|-------------|
| `query` | Search term for PubMed |
| `-n`, `--num_results` | Number of results (default: 5) |
| `-f`, `--file` | Output filename (default: output.csv) |
| `-d`, `--debug` | Enable debug mode |

### Example Output
```plaintext
================= PubMed Research Paper Fetcher =================
🔍 Searching for papers related to: **cancer treatment**
📡 Fetching papers from PubMed API...
✅ Successfully fetched 10 papers.
💾 Saving papers to file: results.csv ...
✅ Processing complete. Results saved!
```

## 📦 Packaging & Publishing

### 🔹 Build the Package

```sh
poetry build
```

### 🔹 Publish to TestPyPI

```sh
poetry publish -r testpypi
```

### 🔹 Install from TestPyPI

```sh
pip install --index-url https://test.pypi.org/simple/ pubmed-paper-fetcher-vivek
```

---

## 🛠 Running Tests

```sh
pytest tests/
```

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m "Added feature xyz"`)
4. Push to your branch (`git push origin feature-xyz`)
5. Open a Pull Request

---

## 📧 Contact

For queries, contact **Vivek Ranjan Sahoo** at: [**vivekranjansahoo81@gmail.com**](mailto\:vivekranjansahoo81@gmail.com)

🚀 **Happy Coding!** 🚀

