from typing import Optional

def create_vertex_url(
    vertex_location: str,
    vertex_project: str,
    stream: Optional[bool],
    model: str,
    api_base: Optional[str] = None,
) -> str:
    """Return the api base for vertex model garden (without /chat/completions)."""
    base_url = get_vertex_base_url(vertex_location)
    if _vertex_model_garden_model_id_in_json_body(model):
        return (
            f"{base_url}/v1/projects/{vertex_project}/locations/{vertex_location}"
            "/endpoints/openapi"
        )
    return f"{base_url}/v1beta1/projects/{vertex_project}/locations/{vertex_location}/endpoints/{model}"

