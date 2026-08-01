
def _map_openai_size_to_vertex_ai_aspect_ratio(size: Optional[str]) -> str:
    """Map OpenAI size parameter to Vertex AI aspectRatio."""
    if size is None:
        return "1:1"

    # Map OpenAI size strings to Vertex AI aspect ratio strings
    # Vertex AI accepts: "1:1", "9:16", "16:9", "4:3", "3:4"
    size_to_aspect_ratio = {
        "256x256": "1:1",  # Square
        "512x512": "1:1",  # Square
        "1024x1024": "1:1",  # Square (default)
        "1792x1024": "16:9",  # Landscape
        "1024x1792": "9:16",  # Portrait
    }
    return size_to_aspect_ratio.get(
        size, "1:1"
    )  # Default to square if size not recognized

