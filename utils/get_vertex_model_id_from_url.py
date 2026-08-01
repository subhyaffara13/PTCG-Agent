
def get_vertex_model_id_from_url(url: str) -> Optional[str]:
    """
    Get the vertex model id from the url

    `https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/${MODEL_ID}:streamGenerateContent`
    """
    match = re.search(r"/models/([^:]+)", url)
    return match.group(1) if match else None

