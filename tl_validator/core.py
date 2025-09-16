# tl_validator/core.py
import json
import os
import typing as t
import re as _re

# ------- Defaults & env toggles -------
DEFAULTS = {
    "threshold": "low",
    "operator": "or",
    "page_limit": 50,
    "group_by": "clip",
    "search_options": ["visual", "audio"],
}

HAS_REAL_FILTERS = os.getenv("TL_REAL_FILTERS") == "1"
HAS_IMAGE_URL = os.getenv("TL_IMAGE_URL") == "1"

NEEDS_REAL_FILTERS = {
    "Filter by filename (system metadata)",
    "Filter by duration range",
    "Filter by video id list",
    "User metadata boolean filter",
}
NEEDS_IMAGE_URL = {
    "Image search with URL (if image search enabled)",
}

# ------- Pytest output parsing (precompiled regex) -------
_RE_FAILED_SUMMARY = _re.compile(r"-\s+Failed:\s*(.*)$")
_RE_FAILED_TRACE = _re.compile(r"^E\s+Failed:\s*(.*)$")
_RE_PROGRESS = _re.compile(r"\[\s*100%\s*]$")
_RE_SUMMARY_LINE = _re.compile(
    r"^\d+\s+(passed|failed|skipped|xfailed|xpassed|errors?)\b.*in\s+[0-9.]+s"
)


def extract_simple_failures(text: str) -> list[str]:
    msgs: list[str] = []
    for ln in text.splitlines():
        ln = ln.rstrip()
        m = _RE_FAILED_SUMMARY.search(ln) or _RE_FAILED_TRACE.match(ln)
        if m:
            msgs.append(m.group(1))
    seen: set[str] = set()
    uniq: list[str] = []
    for m in msgs:
        if m not in seen:
            seen.add(m)
            uniq.append(m)
    return uniq


def extract_progress_and_summary(stdout: str) -> tuple[str, str]:
    progress = ""
    summary = ""
    for ln in (stdout or "").splitlines():
        if _RE_PROGRESS.search(ln):
            progress = ln.rstrip()
        if _RE_SUMMARY_LINE.search(ln):
            summary = ln.rstrip()
    return progress, summary


# ------- Cases file loading (lazy + robust path resolution) -------
def _resolve_cases_path() -> str:
    """
    Precedence:
      1) TL_CASES_FILE (absolute or relative)
      2) ./advanced_test_cases.json
      3) ./test_cases.json
      4) ./test_cases_json/advanced_test_cases.json
      5) ./test_cases_json/test_cases.json
    """
    import pathlib as _pl
    candidates = []
    env_p = os.getenv("TL_CASES_FILE")
    if env_p:
        candidates.append(env_p)
    candidates.extend([
        "advanced_test_cases.json",
        "test_cases.json",
        os.path.join("test_cases_json", "advanced_test_cases.json"),
        os.path.join("test_cases_json", "test_cases.json"),
    ])
    for c in candidates:
        p = _pl.Path(c).expanduser().resolve()
        if p.exists():
            return str(p)
    raise FileNotFoundError(
        "Could not find a cases JSON file. Set TL_CASES_FILE or place one of: "
        "advanced_test_cases.json, test_cases.json, test_cases_json/advanced_test_cases.json, "
        "test_cases_json/test_cases.json in the project root."
    )


def load_cases() -> t.List[dict]:
    path = _resolve_cases_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------- IDs for pytest parametrize -------
def ids(cases: t.List[dict]) -> t.List[str]:
    return [
        c.get("description")
        or c.get("query_text")
        or c.get("query_media_url")
        or f"case_{i}"
        for i, c in enumerate(cases)
    ]


# ------- Search helpers -------
def _extract_items(res) -> t.List[object]:
    items = getattr(res, "items", None)
    if isinstance(items, list) and items:
        return items
    if hasattr(res, "__iter__") and not isinstance(res, (dict, str, bytes)):
        collected: t.List[object] = []
        for it in res:
            page_items = getattr(it, "items", None)
            if isinstance(page_items, list):
                collected.extend(page_items)
            else:
                collected.append(it)
        if collected:
            return collected
    for attr in ("data", "clips"):
        val = getattr(res, attr, None)
        if isinstance(val, list) and val:
            return val
    return []


def _build_kwargs(case: dict) -> dict:
    kw: dict = {
        "threshold": case.get("threshold", DEFAULTS["threshold"]),
        "operator": case.get("operator", DEFAULTS["operator"]),
        "page_limit": case.get("page_limit", DEFAULTS["page_limit"]),
        "group_by": case.get("group_by", DEFAULTS["group_by"]),
        "search_options": case.get("search_options", DEFAULTS["search_options"]),
    }
    if isinstance(case.get("filter"), str):
        kw["filter"] = case["filter"]
    if case.get("query_media_type") == "image":
        kw["query_media_type"] = "image"
        if case.get("query_media_url"):
            kw["query_media_url"] = case["query_media_url"]
        kw["query_text"] = None
    else:
        qtext = case.get("query_text")
        kw["query_text"] = None if qtext is None else str(qtext)
    return kw


def classify(client, index_id: str, case: dict) -> t.Tuple[str, t.List[object], str]:
    """Return ('hits'|'no_hits'|'error', items, reason)."""
    try:
        kwargs = _build_kwargs(case)
        res = client.search.query(index_id=index_id, **kwargs)
        items = _extract_items(res)
        return ("hits" if items else "no_hits", items, "")
    except Exception as exc:  # noqa: BLE001
        status = getattr(exc, "status", None) or getattr(exc, "status_code", None)
        code = getattr(exc, "code", None)
        body = getattr(exc, "body", None)
        msg = ""
        if isinstance(body, dict):
            msg = body.get("message") or body.get("detail") or ""
        parts = [str(x) for x in (status, code, msg) if x]
        return ("error", [], " / ".join(parts) or exc.__class__.__name__)


def assert_match(case: dict, expected: t.Union[bool, str], actual: str, reason: str) -> None:
    target = {True: "hits", False: "no_hits", "error": "error"}[expected]
    if actual != target:
        import pytest  # local import to keep this module runner-free
        label = case.get("description") or case.get("query_text") or str(case)
        detail = f" (reason: {reason})" if reason else ""
        pytest.fail(f"{label!r}: expected {target}, got {actual}{detail}")


def validate_with_fallbacks(
    client, index_id: str, case: dict
) -> t.Tuple[str, t.List[object], str]:
    if case.get("query_media_type") == "image":
        return classify(client, index_id, case)
    base = case.get("query_text")
    if base is None:
        return classify(client, index_id, case)
    last: t.Tuple[str, t.List[object], str] = classify(client, index_id, case)
    for q in (base, str(base).lower(), str(base).title()):
        for opts in (["visual", "audio"], ["visual"], ["audio"]):
            alt = {**case, "query_text": q, "search_options": opts}
            actual, items, reason = classify(client, index_id, alt)
            if actual == "hits":
                return actual, items, reason
            last = (actual, items, reason)
    return last
