
def normalize_key(key: str) -> str:
    # e.g "content-type" -> "content_type", "Accept" -> "accept"
    return key.replace("-", "_").replace(" ", "_").lower()

