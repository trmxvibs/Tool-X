"""
Data-integrity tests for core/data.json (loaded via core.tool_data).

Updated: 17/08/2026 (new file)

With 1006+ tool entries maintained by hand and via PRs, the biggest
real risk isn't the Python logic — it's a malformed or incomplete
entry slipping in (missing URL, empty name, bad category reference).
These tests catch that class of bug in CI before merge.
"""
from core.tool_data import RAW_TOOLS, TOOL_CATEGORIES, TOOLS_BY_CATEGORY

VALID_PACKAGE_MANAGERS = {"git", "curl"}


def test_tool_database_is_not_empty():
    assert len(RAW_TOOLS) > 0


def test_every_tool_has_a_name():
    missing = [key for key, data in RAW_TOOLS.items() if not data.get("name")]
    assert not missing, f"Tools missing 'name': {missing[:10]}"


def test_every_tool_has_a_url():
    missing = [key for key, data in RAW_TOOLS.items() if not data.get("url")]
    assert not missing, f"Tools missing 'url': {missing[:10]}"


def test_every_tool_url_looks_like_a_url():
    bad = [
        key for key, data in RAW_TOOLS.items()
        if not str(data.get("url", "")).startswith(("http://", "https://"))
    ]
    assert not bad, f"Tools with non-http(s) url: {bad[:10]}"


def test_every_tool_has_a_known_package_manager():
    bad = [
        key for key, data in RAW_TOOLS.items()
        if data.get("package_manager") not in VALID_PACKAGE_MANAGERS
    ]
    assert not bad, f"Tools with unrecognized package_manager: {bad[:10]}"


def test_no_exact_duplicate_urls():
    """
    Two different tool keys pointing at the identical repo URL is a
    likely duplicate (e.g. same repo listed twice with different
    casing or a trailing .git). Similar-looking names for genuinely
    different repos are fine and common in this ecosystem — only an
    identical normalized URL counts here.

    3 pairs already exist in the current dataset (same repo, listed
    under two names) — that's a content cleanup decision for the
    maintainer, not something CI should block on. They're allowlisted
    below so this test's real job is catching any *new* accidental
    duplicate before it merges.
    """
    def normalize(url):
        return str(url).rstrip("/").removesuffix(".git").lower()

    KNOWN_EXISTING_DUPES = {
        frozenset({"findomain", "Findomain"}),
        frozenset({"fbi", "FBI-tools"}),
        frozenset({"fierce", "FiercePhish"}),
    }

    seen = {}
    new_dupes = []
    for key, data in RAW_TOOLS.items():
        url = normalize(data.get("url", ""))
        if not url:
            continue
        if url in seen:
            pair = frozenset({seen[url], key})
            if pair not in KNOWN_EXISTING_DUPES:
                new_dupes.append((seen[url], key, url))
        seen[url] = key
    assert not new_dupes, f"New duplicate tool entries pointing at the same repo: {new_dupes[:10]}"


def test_tool_categories_is_not_empty():
    assert len(TOOL_CATEGORIES) > 0


def test_every_category_has_at_least_one_tool():
    empty = [
        cat_id for cat_id, cat_name in TOOL_CATEGORIES.items()
        if not TOOLS_BY_CATEGORY.get(cat_name)
    ]
    assert not empty, f"Categories with zero tools: {empty}"


def test_every_tool_has_at_least_one_category():
    """Raw category field (pre-cleaning) should never be empty/missing."""
    missing = [
        key for key, data in RAW_TOOLS.items()
        if not data.get("category") or data["category"] == [None]
    ]
    # These fall back to "uncategorized" by design (see tool_data.clean_category_name),
    # so this isn't a hard failure — just tracked so the count doesn't silently grow.
    assert len(missing) < 50, (
        f"{len(missing)} tools have no category — more than expected, "
        f"first few: {missing[:10]}"
    )
