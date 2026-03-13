# TwelveLabs API Validator

Python validation framework for testing multimodal search behavior against the TwelveLabs Search API.

This repo uses pytest plus JSON-defined test cases to validate search behavior across normal queries, edge cases, multilingual inputs, and expected error scenarios. It also includes a lightweight runner that can execute one file or an entire folder of case definitions and save timestamped reports for review.

## Why This Exists

I built this project to show a style of engineering I care about:

- test behavior, not just implementation
- separate test logic from test data
- make edge cases easy to add
- produce artifacts that are useful after the test run finishes

It is a validation framework, not just a small script collection.

## What It Tests

The suite validates cases such as:

- normal semantic search queries
- low-hit and no-hit behavior
- expected API error behavior
- fuzzy matching and query variation fallback
- internationalization scenarios
- optional real-filter cases
- optional image-search cases

## Design Highlights

### JSON-driven cases

Test definitions live in [test_cases_json](/Users/chrisyoon/GitHub/TwelveLabs/test_cases_json), which means new scenarios can be added without changing the assertion engine.

### Shared validation core

[tl_validator/core.py](/Users/chrisyoon/GitHub/TwelveLabs/tl_validator/core.py) handles:

- case loading
- path resolution
- search request construction
- result classification
- fallback retries for text queries
- simple failure extraction for reporting

### Runner and reporting

[tl_validator/runner.py](/Users/chrisyoon/GitHub/TwelveLabs/tl_validator/runner.py) can:

- select a single JSON file
- select a folder of JSON files
- execute pytest in batch mode
- extract progress and summary lines
- write timestamped report files to `validation_results/`

## Repo Structure

```text
TwelveLabs/
├── tl_validator/
│   ├── core.py
│   └── runner.py
├── tests/
│   └── test_search.py
├── test_cases_json/
│   ├── advanced_test_cases.json
│   ├── negative_test_cases.json
│   └── positive_test_cases.json
├── validation_results/
├── requirements.txt
└── pytest.ini
```

## Running Locally

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file with:

```env
TWELVE_LABS_API_KEY=your_api_key
TWELVE_LABS_INDEX_ID=your_index_id
```

Optional flags:

```env
TL_REAL_FILTERS=1
TL_IMAGE_URL=1
TL_INCLUDE_FULL_OUTPUT=1
```

### 3. Run the pytest suite

```bash
pytest -q
```

### 4. Run the standalone runner

```bash
python -m tl_validator.runner
```

## What This Repo Demonstrates

- Python test framework design
- data-driven validation patterns
- API behavior testing
- edge-case thinking
- report generation for manual review and auditability

## Hiring Signal

This project is useful because it shows I do not stop at “the request returned 200.”

I care about:

- how systems behave at the edges
- how test definitions scale
- how to make validation readable, reusable, and operationally useful
