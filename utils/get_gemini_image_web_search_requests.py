from typing import Any, Dict, List, Optional

def get_gemini_image_web_search_requests(
    response_data: Dict[str, Any],
) -> Optional[int]:
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    grounding_metadata: List[Dict[str, Any]] = []
    for candidate in response_data.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        candidate_grounding = candidate.get("groundingMetadata")
        if isinstance(candidate_grounding, list):
            grounding_metadata.extend(candidate_grounding)
        elif isinstance(candidate_grounding, dict):
            grounding_metadata.append(candidate_grounding)

    return VertexGeminiConfig._calculate_web_search_requests(grounding_metadata)

