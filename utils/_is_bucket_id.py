
def _is_bucket_id(argument: str) -> bool:
    """Check if argument is a bucket ID (namespace/name) vs just a namespace."""
    if argument.startswith(BUCKET_PREFIX):
        path = argument[len(BUCKET_PREFIX) :]
    else:
        path = argument
    return "/" in path

