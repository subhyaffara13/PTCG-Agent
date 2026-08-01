
def _reload_prompt_in_registry(
    registry: Any, versioned_id: str, updated_prompt_spec: PromptSpec
) -> PromptSpec:
    """Remove stale entry and re-initialize the prompt in the in-memory registry."""
    if versioned_id in registry.IN_MEMORY_PROMPTS:
        del registry.IN_MEMORY_PROMPTS[versioned_id]
    if versioned_id in registry.prompt_id_to_custom_prompt:
        del registry.prompt_id_to_custom_prompt[versioned_id]
    initialized = registry.initialize_prompt(
        prompt=updated_prompt_spec, config_file_path=None
    )
    if initialized is None:
        raise HTTPException(status_code=500, detail="Failed to patch prompt")
    return initialized

