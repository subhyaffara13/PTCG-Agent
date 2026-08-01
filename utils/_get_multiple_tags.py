
def _get_multiple_tags(params: str) -> tuple[list[str], str]:
    """Check for multiple tags when the title is double quoted."""
    re_tags = re.compile(r'^\s*(?P<tokens>[^"]+)\s+"(?P<title>.*)"\S*$')
    match = re_tags.match(params)
    if match:
        tags = match["tokens"].strip().split(" ")
        return [tag.lower() for tag in tags], match["title"]
    raise ValueError("No match found for parameters")

