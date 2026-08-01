
def _container_model_object_id(
    original_container_id: str, custom_llm_provider: str
) -> str:
    return f"{CONTAINER_OBJECT_PURPOSE}:{custom_llm_provider}:{original_container_id}"

