
def has_test_name_tag(name: str, tag: str) -> bool:
    """Check if a test case name contains a tag token like ``_experimental``.

    A tag matches if it appears as a full underscore-delimited token:
    ``foo_tag_bar`` or ``foo_tag``.
    """
    return re.search(rf"(?:^|_){re.escape(tag)}(?:_|$)", name) is not None

