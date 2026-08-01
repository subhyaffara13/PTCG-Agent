
def get_latest_prompt_versions(prompts: List[PromptSpec]) -> List[PromptSpec]:
    """
    Filter a list of prompts to return only the latest version of each unique prompt.

    Args:
        prompts: List of PromptSpec objects

    Returns:
        List of PromptSpec objects with only the latest version of each prompt
    """
    latest_prompts: Dict[str, PromptSpec] = {}

    for prompt in prompts:
        base_id = get_base_prompt_id(prompt_id=prompt.prompt_id)
        version = get_version_number(prompt_id=prompt.prompt_id)

        # Keep the prompt with the highest version number
        if base_id not in latest_prompts:
            latest_prompts[base_id] = prompt
        else:
            existing_version = get_version_number(
                prompt_id=latest_prompts[base_id].prompt_id
            )
            if version > existing_version:
                latest_prompts[base_id] = prompt

    return list(latest_prompts.values())

