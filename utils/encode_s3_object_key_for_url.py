
def encode_s3_object_key_for_url(object_key: str) -> str:
    return quote(unquote(object_key), safe="/")

