
def is_base64_encoded(s: str) -> bool:
    try:
        # Strip out the prefix if it exists
        if not s.startswith(
            "data:"
        ):  # require `data:` for base64 str, like openai. Prevents false positives like s='Dog'
            return False

        s = s.split(",")[1]

        # Try to decode the string
        decoded_bytes = base64.b64decode(s, validate=True)

        # Check if the original string can be re-encoded to the same string
        return base64.b64encode(decoded_bytes).decode("utf-8") == s
    except Exception:
        return False

