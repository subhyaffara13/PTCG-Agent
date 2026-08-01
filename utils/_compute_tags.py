
def _compute_tags(original_tags: Iterable[str], new_tags: str | None) -> set[str]:
    """Add or replace tags. Supports dot-separated tags"""
    if new_tags is None:
        return set(original_tags)

    if new_tags.startswith("+"):
        return {*original_tags, *new_tags[1:].split(".")}

    if new_tags.startswith("-"):
        return set(original_tags) - set(new_tags[1:].split("."))

    return set(new_tags.split("."))

