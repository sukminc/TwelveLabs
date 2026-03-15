# CLAUDE.md — TwelveLabs API Validator

## Repo Role

Archive proof-of-work repo for API validation and test framework design.

This repo is not part of the poker hub.
Its value is showing clear validation engineering:

- JSON-defined test cases
- reusable validation core
- edge-case coverage
- report generation

## Guardrails

- Keep the repo framed as a validation framework, not a generic script bundle.
- Preserve the test-data-separate-from-test-logic pattern.
- Do not overcomplicate the story beyond observable API behavior and framework design.

## Current Truth

Trust `README.md` for implementation details and usage.

Primary signal:

- boundary validation
- data-driven test definitions
- multilingual and fuzzy-match coverage
- reusable runner outputs

## Commands

```bash
pip install -r requirements.txt
pytest
pytest -v tests/
```
