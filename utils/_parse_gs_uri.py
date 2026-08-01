
def _parse_gs_uri(gs_uri: str) -> Tuple[str, str]:
    if not gs_uri.startswith("gs://"):
        raise ValueError(f"Invalid gs URI: {gs_uri}")
    uri_without_scheme = gs_uri[5:]  # drop gs://
    uri_parts = uri_without_scheme.split("/", 1)
    if len(uri_parts) != 2 or not uri_parts[0] or not uri_parts[1]:
        raise ValueError(f"Invalid gs URI: {gs_uri}")
    return uri_parts[0], uri_parts[1]

