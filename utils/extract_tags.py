from typing import Any, Dict, List, Optional

def extract_tags(
    opik_metadata: Dict[str, Any],
    custom_llm_provider: Optional[str],
) -> List[str]:
    """
    Extract and build list of tags.

    Args:
        opik_metadata: Opik metadata dictionary
        custom_llm_provider: LLM provider name to add as tag

    Returns:
        List of tags
    """
    tags = list(opik_metadata.get("tags", []))

    if custom_llm_provider:
        tags.append(custom_llm_provider)

    return tags

