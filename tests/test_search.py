# tests/test_search.py
import typing as t
import pytest
from tl_validator.core import (
    load_cases, ids, classify, assert_match, validate_with_fallbacks,
    HAS_REAL_FILTERS, HAS_IMAGE_URL, NEEDS_REAL_FILTERS, NEEDS_IMAGE_URL,
)

TEST_CASES: t.List[dict] = load_cases()
_VALIDATION_CASES = [c for c in TEST_CASES if c.get("expected_outcome") in (True, False)]
_ERROR_CASES = [c for c in TEST_CASES if c.get("expected_outcome") == "error"]


@pytest.mark.parametrize("case", _VALIDATION_CASES, ids=ids(_VALIDATION_CASES))
def test_search_api_validation(client, index_id, case):
    desc = case.get("description", "")
    if desc in NEEDS_REAL_FILTERS and not HAS_REAL_FILTERS:
        pytest.xfail(f"env not configured for: {desc}")
    if desc in NEEDS_IMAGE_URL and not HAS_IMAGE_URL:
        pytest.xfail(f"env not configured for: {desc}")

    expected = case["expected_outcome"]
    actual, _items, reason = classify(client, index_id, case)
    if actual == "no_hits" and case.get("query_media_type") != "image":
        actual, _items, reason = validate_with_fallbacks(client, index_id, case)
    assert_match(case, expected, actual, reason)


@pytest.mark.parametrize("case", _ERROR_CASES, ids=ids(_ERROR_CASES))
def test_search_api_error_behaviors(client, index_id, case):
    desc = case.get("description", "")
    if desc in NEEDS_IMAGE_URL and not HAS_IMAGE_URL:
        pytest.xfail(f"env not configured for: {desc}")

    actual, _items, reason = classify(client, index_id, case)
    if actual not in {"error", "no_hits"}:
        assert_match(case, "error", actual, reason)
