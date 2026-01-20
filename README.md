# TwelveLabs Search API Validation Tool

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-7.0+-green.svg)](https://docs.pytest.org/)
[![Code Style: Flake8](https://img.shields.io/badge/code%20style-flake8-black.svg)](https://flake8.pycqa.org/)

> **Architected for Reliability:** A data-driven validation framework ensuring the integrity of TwelveLabs' multimodal video search capabilities via their Python SDK.

This project provides a comprehensive **pytest-based validation suite** and a **custom standalone GUI runner** to test the TwelveLabs Search API. It is designed to simulate real-world usage patterns, validate edge cases (fuzzy matching, internationalization), and enforce rigorous data integrity checks.

---

## 📋 Key Features

### 🔍 Automated Data-Driven Validation
- **JSON-Driven Architecture:** Decouples test logic from test data, allowing non-technical stakeholders to define scenarios in `test_cases_json/` without touching code.
- **Dynamic Assertions:** automatically classifies expected outcomes (Boolean hits vs. Error states).

### 🛠 Flexible Execution Models
- **CLI Standard Mode:** Native `pytest` integration for CI/CD pipelines.
- **GUI Standalone Runner:** A custom Tkinter-based runner allowing batch execution via file/folder selection for ad-hoc testing.

### 🌍 Comprehensive Test Coverage
- **Linguistic Robustness:** Validates plurals, case variations, and fuzzy matching.
- **Internationalization (i18n):** Verified support for Korean, Japanese, Arabic, and other non-Latin scripts.
- **Edge Case Handling:** Punctuation, emojis, whitespace-only queries, and injection attempts.
- **Multimedia Support:** Optional toggles for Image-to-Video search validation.

### 📊 Smart Reporting System
- **Timestamped Artifacts:** Auto-generates detailed `.txt` reports in `validation_results/` for audit trails.
- **Summary Metrics:** Provides instant pass/fail counts and exit codes for pipeline integration.
- **Debug-Friendly:** Options to capture full `stdout`/`stderr` for deep-dive root cause analysis.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- A TwelveLabs API Key and Index ID (Sign up at the [TwelveLabs Playground](https://playground.twelvelabs.io/))

### Installation

1.  **Clone the repository**
    ```sh
    git clone [https://github.com/sukminc/TwelveLabs.git](https://github.com/sukminc/TwelveLabs.git)
    cd TwelveLabs
    ```

2.  **Set up the environment**
    Create a `.env` file in the project root:
    ```env
    TWELVE_LABS_API_KEY="your_api_key_here"
    TWELVE_LABS_INDEX_ID="your_index_id_here"
    ```

3.  **Install Dependencies**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

---

## ▶️ Usage Guide

### 1. Standard Pytest Execution (CLI)
Ideal for CI/CD pipelines or quick sanity checks.

```sh
pytest -q

```

### 2. Standalone Runner (GUI/Batch)

Best for testing specific datasets or running extensive regression suites.

```sh
python -m tl_validator.runner

```

* **Prompt:** "Do you want to run all JSON files in a folder?"
* **Yes:** Opens a folder picker to run batch tests.
* **No:** Opens a file picker to select specific `.json` test definitions.



---

## 🧪 Test Case Definitions

Test scenarios are defined in strictly typed JSON files located in `test_cases_json/`.

**Example `simple_noun.json`:**

```json
{
  "description": "Basic semantic search for objects",
  "query_text": "Golden Retriever",
  "expected_outcome": true,
  "filter": {
      "duration": { "gte": 10 }
  }
}

```

| Field | Type | Description |
| --- | --- | --- |
| `description` | `str` | Human-readable context for the test case. |
| `query_text` | `str` | The actual search query sent to the API. |
| `expected_outcome` | `bool | "error"` | `true` (≥1 hit), `false` (0 hits), or `"error"` (API should reject). |
| `filter` | `dict` | (Optional) Metadata filters to apply. |

---

## ⚙️ Advanced Configuration

Control test behaviour using environment variables:

* `TL_REAL_FILTERS=1`: Enable tests that require specific metadata in your index.
* `TL_IMAGE_URL=1`: Enable Image-to-Video search tests (requires valid image URLs).
* `TL_INCLUDE_FULL_OUTPUT=1`: Append full Pytest `stdout`/`stderr` to the report files.
* `TL_CASES_FILE=/path/to/custom.json`: Override the default test source programmatically.

---

## 📂 Project Architecture

```
TwelveLabs/
├── tl_validator/           # Core Framework Logic
│   ├── core.py             # Heuristics, classifiers, and assertion logic
│   └── runner.py           # GUI & CLI Batch Orchestrator
├── tests/
│   └── test_search.py      # Pytest entry point
├── test_cases_json/        # Data-driven test definitions
├── validation_results/     # Automated report artifacts
├── .env                    # Secrets (Excluded from Git)
└── requirements.txt        # Dependency manifest

```

---

## 📊 Reporting & result Analysis

Results are saved to `validation_results/YYYYMMDD_HHMMSS_<filename>.txt`.

**Result Symbols:**

* `.` : **Pass** (Assertion met)
* `F` : **Fail** (Assertion mismatch)
* `x` : **XFail** (Known issue/Expected failure)
* `s` : **Skip** (Test skipped via config)

**Sample Report Output:**

```text
Test Suite: advanced_test_cases.json
Status: COMPLETED
--------------------------------------------------
.......xxxx.......x.......... [100%]
--------------------------------------------------
Total: 30 | Passed: 25 | Failed: 0 | XFailed: 5
Report generated at: 2025-09-16 15:12:01

```

---

## 📈 Roadmap

* [x] **Phase 1 (MVP):** Pytest suite, GUI Runner, and Basic Reporting.
* [ ] **Phase 2 (CI/CD):** Jenkins/GitHub Actions integration templates.
* [ ] **Phase 3 (Visualization):** HTML Dashboard for historic trend analysis.

---

## 👤 Author

**Chris (Suk Min) Yoon**

* **Portfolio:** [github.com/sukminc](https://www.google.com/search?q=https://github.com/sukminc)
* **Role:** Lead QA Automation Engineer / Data Quality Specialist

```

```
