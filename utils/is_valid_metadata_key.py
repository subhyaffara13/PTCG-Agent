
def is_valid_metadata_key(text):
    """Can this text be a proper key?"""
    return bool(_IS_VALID_METADATA_KEY.match(text))

