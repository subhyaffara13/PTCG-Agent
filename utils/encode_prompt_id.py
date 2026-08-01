
def encode_prompt_id(raw_id: str) -> str:
    """Convert GitLab path IDs like 'invoice/extract' → 'gitlab::invoice::extract'"""
    if raw_id.startswith(GITLAB_PREFIX):
        return raw_id  # already encoded
    return f"{GITLAB_PREFIX}{raw_id.replace('/', '::')}"

