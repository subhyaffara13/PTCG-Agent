
def encode_gcs_object_name_for_url(object_name: str) -> str:
    return quote(unquote(object_name), safe="")

