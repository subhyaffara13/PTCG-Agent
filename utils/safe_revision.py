
def safe_revision(revision: str) -> str:
    return revision if SPECIAL_REFS_REVISION_REGEX.match(revision) else safe_quote(revision)

