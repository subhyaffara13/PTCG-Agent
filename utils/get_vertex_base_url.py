import re
from typing import Optional

def get_vertex_base_url(vertex_location: Optional[str]) -> str:
    """
    Base URL for Vertex AI pass-through (trailing slash for URL joining).

    Keep location rules aligned with ``litellm.llms.vertex_ai.common_utils.get_vertex_base_url``.
    """
    if vertex_location == "global":
        return "https://aiplatform.googleapis.com/"
    if vertex_location is None:
        raise ValueError("vertex_location is required")
    if not re.match(r"^[a-z][a-z0-9-]*$", vertex_location):
        raise ValueError("Invalid vertex_location format")
    if "-" not in vertex_location:
        return f"https://aiplatform.{vertex_location}.rep.googleapis.com/"
    return f"https://{vertex_location}-aiplatform.googleapis.com/"


def get_vertex_base_url(
    vertex_location: Optional[str],
) -> str:
    """
    Get the base URL for Vertex AI API calls.

    - ``global`` uses the global control plane host.
    - Multi-region geographies (e.g. ``us``, ``eu``) use ``aiplatform.{geo}.rep.googleapis.com``.
    - Regional locations (e.g. ``us-central1``) use ``{region}-aiplatform.googleapis.com``.
    """
    if vertex_location == "global":
        return "https://aiplatform.googleapis.com"
    if vertex_location is None:
        raise ValueError("vertex_location is required")
    if not re.match(r"^[a-z][a-z0-9-]*$", vertex_location):
        raise ValueError("Invalid vertex_location format")
    if "-" not in vertex_location:
        return f"https://aiplatform.{vertex_location}.rep.googleapis.com"
    return f"https://{vertex_location}-aiplatform.googleapis.com"

