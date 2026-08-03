from typing import Any, Dict

def get_latest_version_prompt_id(prompt_id: str, all_prompt_ids: Dict[str, Any]) -> str:
    """
    Find the latest version of a prompt from available prompt IDs.

    Args:
        prompt_id: Base prompt ID or versioned prompt ID (e.g., "jack_success" or "jack_success.v2")
        all_prompt_ids: Dictionary of all available prompt IDs (keys are prompt IDs)

    Returns:
        The prompt ID with the highest version number, or the original prompt_id if no versions exist

    Examples:
        >>> all_ids = {"jack.v1": {}, "jack.v2": {}, "jack.v3": {}}
        >>> get_latest_version_prompt_id("jack", all_ids)
        "jack.v3"
        >>> get_latest_version_prompt_id("jack.v1", all_ids)
        "jack.v3"
        >>> all_ids = {"simple": {}}
        >>> get_latest_version_prompt_id("simple", all_ids)
        "simple"
    """
    base_id = get_base_prompt_id(prompt_id=prompt_id)

    # Find all versions of this prompt
    matching_versions = []
    for stored_prompt_id in all_prompt_ids.keys():
        if get_base_prompt_id(prompt_id=stored_prompt_id) == base_id:
            version_num = get_version_number(prompt_id=stored_prompt_id)
            matching_versions.append((version_num, stored_prompt_id))

    # Use the highest version number
    if matching_versions:
        matching_versions.sort(reverse=True)
        return matching_versions[0][1]
    else:
        # No versioned prompts found, use the base ID as-is
        return prompt_id

