
def create_versioned_prompt_spec(db_prompt) -> PromptSpec:
    """
    Helper function to create a PromptSpec with versioned prompt_id from a DB prompt entry.

    Args:
        db_prompt: The DB prompt object (from prisma)

    Returns:
        PromptSpec with versioned prompt_id (e.g., "chat_prompt.v1")
    """
    import json

    from litellm.types.prompts.init_prompts import PromptLiteLLMParams

    prompt_dict = db_prompt.model_dump()
    base_prompt_id = prompt_dict["prompt_id"]
    version = prompt_dict.get("version", 1)
    environment = prompt_dict.get("environment", "development")
    created_by = prompt_dict.get("created_by")

    # Parse litellm_params
    litellm_params_data = prompt_dict.get("litellm_params")
    if isinstance(litellm_params_data, str):
        litellm_params_data = json.loads(litellm_params_data)
    litellm_params = PromptLiteLLMParams(**litellm_params_data)

    # Parse prompt_info
    prompt_info_data = prompt_dict.get("prompt_info")
    if prompt_info_data:
        if isinstance(prompt_info_data, str):
            prompt_info_data = json.loads(prompt_info_data)
        prompt_info = PromptInfo(**prompt_info_data)
    else:
        prompt_info = PromptInfo(prompt_type="db")

    # Create versioned prompt_id
    versioned_prompt_id = f"{base_prompt_id}.v{version}"

    return PromptSpec(
        prompt_id=versioned_prompt_id,
        litellm_params=litellm_params,
        prompt_info=prompt_info,
        created_at=prompt_dict.get("created_at"),
        updated_at=prompt_dict.get("updated_at"),
        environment=environment,
        created_by=created_by,
    )

