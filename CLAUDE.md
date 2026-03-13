# CLAUDE.md — TwelveLabs API Validator

## Brand Hub
**onepercentbetter.poker** — this project is listed there as `TwelveLabs API Validator`.
If it's removed from the site, it's no longer a brand asset.
Owner: Chris S. Yoon · github.com/sukminc

## What this is
JSON-driven validation suite for the TwelveLabs multimodal video search API.
Status: `live` (100% MVP)
Slug on hub: `twelvelabs-validator` · Repo: `sukminc/TwelveLabs`

## Core Value
Production-quality test framework — decouples test logic from test data.
Demonstrates observability mindset: validate at the boundary, surface all edge cases.

## Stack
- Python + Pytest
- TwelveLabs SDK

## Key Architecture
- JSON-driven: test cases defined as data, not hardcoded in test functions
- Covers linguistic edge cases: plurals, i18n (Korean/Japanese/Arabic)
- Fuzzy matching + injection attempt coverage
- Built to production observability standard, not throwaway scripts

## Commands
```bash
pip install -r requirements.txt
pytest                         # run full suite
pytest -v tests/               # verbose
```
