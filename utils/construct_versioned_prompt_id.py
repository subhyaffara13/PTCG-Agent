from typing import Optional

def construct_versioned_prompt_id(prompt_id: str, version: Optional[int] = None) -> str:
    """
    Construct a versioned prompt ID from a base prompt_id and version number.

    Args:
        prompt_id: Base prompt ID (e.g., "jack_success")
        version: Version number (if None, returns the base prompt_id unchanged)

    Returns:
        Versioned prompt ID (e.g., "jack_success.v4")

    Examples:
        >>> construct_versioned_prompt_id("jack_success", 4)
        "jack_success.v4"
        >>> construct_versioned_prompt_id("jack_success", None)
        "jack_success"
        >>> construct_versioned_prompt_id("jack_success.v2", 4)
        "jack_success.v4"
    """
    if version is None:
        return prompt_id

    # Strip any existing version suffix first
    base_id = get_base_prompt_id(prompt_id)
    return f"{base_id}.v{version}"

