# TwelveLabs Search API Validation Tool

This project provides a pytest-based validation suite and a standalone runner to test the TwelveLabs Search API through its Python SDK. It is built for data-driven validation, ensuring reliable performance, robust error handling, and reproducible results across different query scenarios.

---

## 📋 Overview
- **Automated Validation**  
  Run test cases defined in JSON files (`test_cases_json/*.json`) against a real TwelveLabs index.
- **Flexible Execution**
  - Run tests directly with pytest.
  - Or use the standalone runner with a GUI file/folder picker.
- **Comprehensive Coverage**
  - Common queries, plurals, case variations, and fuzzy matches.
  - Edge cases (punctuation, emojis, whitespace, special characters).
  - Internationalization (Korean, Japanese, Arabic, etc.).
  - Boundary and invalid inputs (empty, whitespace-only, long strings).
  - Optional index-dependent filters and image search.
- **Smart Reporting**
  - Compact pytest progress lines.
  - Timestamped `.txt` reports in `validation_results/`.
  - Simple one-line failure summaries.
  - Optional full stdout/stderr inclusion.

---

## 🚀 Setup
1. **Get Credentials**
   - Sign up at Twelve Labs Playground.
   - Obtain your API Key and create an Index ID with at least one video uploaded.
2. **Configure Environment**  
   Create a `.env` in the project root:

   ```env
   TWELVE_LABS_API_KEY="your_api_key_here"
   TWELVE_LABS_INDEX_ID="your_index_id_here"
   ```

3. **Install Dependencies**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## ▶️ Running Tests

1. **Run via Pytest**

   ```sh
   pytest -q
   ```

2. **Run via Runner (GUI/CLI)**

   ```sh
   python -m tl_validator.runner
   ```
   - Yes → select a folder (all `.json` inside will run).
   - No → select one or more `.json` files.
   - Reports are written into `validation_results/`.

**Example Output**

```
.......xxxx.......x..........                                            [100%]
Saved results to validation_results/20250916_151201_advanced_test_cases.json.txt
FFFFFF.FFFFF.FFFFFFFFF.F..FFs                                            [100%]
Saved results to validation_results/20250916_151213_negative_test_cases.json.txt
```

---

## ⚙️ Environment Toggles
- `TL_REAL_FILTERS=1` → enable index-specific filter/metadata tests.
- `TL_IMAGE_URL=1` → enable image URL tests.
- `TL_INCLUDE_FULL_OUTPUT=1` → include full pytest stdout/stderr in reports.
- `TL_CASES_FILE=/path/to/file.json` → override test case file (used internally by runner).

---

## 📂 Project Structure

```
TwelveLabs/
├─ tl_validator/
│  ├─ core.py        # helpers, defaults, classify/assert logic
│  └─ runner.py      # GUI/CLI batch runner
├─ tests/
│  └─ test_search.py # pytest test suite
├─ test_cases_json/  # JSON files defining test cases
├─ validation_results/ # auto-generated reports
├─ requirements.txt
└─ README.md
```

---

## 🧪 Test Case Format

Each case is a JSON object with:

```json
{
  "description": "Simple noun",
  "query_text": "dog",
  "expected_outcome": true
}
```

- `expected_outcome` can be:
  - `true` → expect ≥1 hit
  - `false` → expect 0 hits
  - `"error"` → expect client/validation error

Optional fields: `query_media_type`, `query_media_url`, `filter`, etc.

---

## 📊 Reports
- Saved in `validation_results/` as:

  ```
  YYYYMMDD_HHMMSS_<cases_filename>.txt
  ```

- Contain:
  - Start/end timestamps
  - Progress and summary lines
  - Simple failure messages
  - (Optional) full pytest output

---

## 🛠 Development Notes
- Code style: flake8 compliant.
- Logic split into core, tests, and runner for clarity.
- GUI runner supports both file and folder selection.