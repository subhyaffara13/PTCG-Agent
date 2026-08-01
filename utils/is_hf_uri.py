
def is_hf_uri(uri: str) -> bool:
    """Check if a string is a valid HF URI ('hf://...') or a recognized Hugging Face web URL."""
    try:
        parse_hf_uri(uri)
        return True
    except HfUriError:
        return False

