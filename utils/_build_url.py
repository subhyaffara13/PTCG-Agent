from typing import Dict

def _build_url(
    api_base: str,
    path_template: str,
    path_params: Dict[str, str],
) -> str:
    """Build the full URL by substituting path parameters.

    The api_base from get_complete_url already includes /containers and may include
    query parameters. We need to parse the URL, append the path, then preserve the
    query parameters.
    """
    # api_base ends with /containers, path_template starts with /containers
    # So we need to strip /containers from the path
    if path_template.startswith("/containers"):
        path_template = path_template[len("/containers") :]

    # Substitute path parameters
    for param, value in path_params.items():
        encoded_value = encode_url_path_segment(value, field_name=param)
        path_template = path_template.replace(f"{{{param}}}", encoded_value)

    # Parse the api_base to extract existing query params
    parsed_base = httpx.URL(api_base)

    # Append the path to the existing path (before query params)
    new_path = f"{parsed_base.path.rstrip('/')}{path_template}"

    # Rebuild URL with new path, preserving query params
    final_url = parsed_base.copy_with(path=new_path)

    return str(final_url)

