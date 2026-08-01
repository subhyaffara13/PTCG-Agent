
def decode_prompt_id(encoded_id: str) -> str:
    """Convert 'gitlab::invoice::extract' → 'invoice/extract'"""
    if not encoded_id.startswith(GITLAB_PREFIX):
        return encoded_id
    return encoded_id[len(GITLAB_PREFIX) :].replace("::", "/")

