
def update_responses_tools_with_model_file_ids(
    tools: Optional[List[Dict[str, Any]]],
    model_id: Optional[str] = None,
    model_file_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
) -> Optional[List[Dict[str, Any]]]:
    """
    Updates responses API tools with provider-specific file IDs.

    Pass 1 (always): decode unified vector_store_ids in file_search tools.
    Pass 2 (needs mapping): map code_interpreter container file_ids to provider IDs.

    Args:
        tools: The responses API tools parameter
        model_id: The model ID to use for looking up provider-specific file IDs
        model_file_id_mapping: Dictionary mapping litellm file IDs to provider file IDs
                               Format: {"litellm_file_id": {"model_id": "provider_file_id"}}
    """
    if not tools or not isinstance(tools, list):
        return tools

    # Pass 1: decode unified vector_store_ids (no mapping needed)
    tools = _decode_vector_store_ids_in_tools(tools) or tools

    # Pass 2: map code_interpreter file IDs (requires mapping)
    if not model_file_id_mapping or not model_id:
        return tools

    updated_tools = []
    for tool in tools:
        if not isinstance(tool, dict):
            updated_tools.append(tool)
            continue

        updated_tool = tool.copy()

        # Handle code_interpreter with container file_ids
        if tool.get("type") == "code_interpreter":
            container = tool.get("container")
            if isinstance(container, dict):
                container_file_ids = container.get("file_ids")
                if isinstance(container_file_ids, list):
                    updated_file_ids = []
                    for file_id in container_file_ids:
                        if isinstance(file_id, str):
                            # Check if we have a mapping for this file ID
                            if file_id in model_file_id_mapping:
                                # Map to provider-specific file ID
                                provider_file_id = (
                                    model_file_id_mapping.get(file_id, {}).get(model_id)
                                    or file_id
                                )
                                updated_file_ids.append(provider_file_id)
                            else:
                                updated_file_ids.append(file_id)
                        else:
                            updated_file_ids.append(file_id)

                    # Update the tool with new file IDs
                    updated_container = container.copy()
                    updated_container["file_ids"] = updated_file_ids
                    updated_tool["container"] = updated_container

        updated_tools.append(updated_tool)

    return updated_tools

