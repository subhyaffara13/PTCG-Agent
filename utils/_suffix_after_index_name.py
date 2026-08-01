
def _suffix_after_index_name(request_path: str, index_name: str) -> Optional[str]:
    """Return the path suffix after ``/indexes/{index_name}``, or None if absent."""
    match = re.search(rf"/indexes/{re.escape(index_name)}(?=$|[/?])", request_path)
    if match is None:
        return None
    return request_path[match.end() :]

