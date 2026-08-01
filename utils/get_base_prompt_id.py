
def get_base_prompt_id(prompt_id: str) -> str:
    """
    Extract the base prompt ID by stripping the version suffix if present.

    Args:
        prompt_id: Prompt ID that may include version suffix (e.g., "jack_success.v1" or "jack_success_v1")

    Returns:
        Base prompt ID without version suffix (e.g., "jack_success")

    Examples:
        >>> get_base_prompt_id("jack_success.v1")
        "jack_success"
        >>> get_base_prompt_id("jack_success_v1")
        "jack_success"
        >>> get_base_prompt_id("jack_success")
        "jack_success"
    """
    # Try dot separator first (.v)
    if ".v" in prompt_id:
        return prompt_id.split(".v")[0]
    # Try underscore separator (_v)
    if "_v" in prompt_id:
        return prompt_id.split("_v")[0]
    return prompt_id

