from typing import Any, Dict, List, Optional

def _decode_vector_store_ids_in_tools(
    tools: Optional[List[Dict[str, Any]]],
) -> Optional[List[Dict[str, Any]]]:
    """
    Decodes unified (LiteLLM-managed) vector_store_ids in file_search tools to
    provider-native IDs.  Non-unified IDs are passed through unchanged.

    This runs unconditionally — no file-ID mapping is required.
    """
    if not tools or not isinstance(tools, list):
        return tools

    from litellm.llms.base_llm.managed_resources.utils import (
        is_base64_encoded_unified_id,
        parse_unified_id,
    )

    updated_tools = []
    for tool in tools:
        if not isinstance(tool, dict) or tool.get("type") != "file_search":
            updated_tools.append(tool)
            continue

        vector_store_ids = tool.get("vector_store_ids")
        if not isinstance(vector_store_ids, list):
            updated_tools.append(tool)
            continue

        decoded_ids = []
        for vs_id in vector_store_ids:
            if not isinstance(vs_id, str) or not is_base64_encoded_unified_id(vs_id):
                decoded_ids.append(vs_id)
                continue

            parsed = parse_unified_id(vs_id)
            provider_resource_id = (
                parsed.get("provider_resource_id") if parsed else None
            )

            if not provider_resource_id:
                verbose_logger.warning(
                    "file_search tool contains unified vector_store_id '%s' that could "
                    "not be decoded to a provider resource ID — passing original ID. "
                    "Ensure the vector store was created via LiteLLM.",
                    vs_id,
                )
                decoded_ids.append(vs_id)
            else:
                decoded_ids.append(provider_resource_id)

        updated_tools.append({**tool, "vector_store_ids": decoded_ids})

    return updated_tools

