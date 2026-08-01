
def _is_bucket_path(path: str) -> bool:
    """Check if a path is a bucket path.

    Do not raise if the path is not a hf:// URI.
    Raise if the path is a hf:// URI but with an incorrect format.
    """
    if not path.startswith(constants.HF_PROTOCOL):
        return False
    return parse_hf_uri(path).is_bucket

