
def _normalize_litellm_params(
    vector_store: LiteLLM_ManagedVectorStore,
) -> LiteLLM_ManagedVectorStore:
    litellm_params = vector_store.get("litellm_params")
    if isinstance(litellm_params, str):
        normalized = LiteLLM_ManagedVectorStore(**dict(vector_store))
        try:
            parsed = json.loads(litellm_params)
            normalized["litellm_params"] = parsed if isinstance(parsed, dict) else {}
        except (TypeError, ValueError):
            normalized["litellm_params"] = {}
        return normalized
    return vector_store


def _normalize_litellm_params(litellm_params: Optional[Any]) -> dict:
    if litellm_params is None:
        return {}
    if isinstance(litellm_params, dict):
        return litellm_params
    if hasattr(litellm_params, "model_dump"):
        try:
            return litellm_params.model_dump()
        except Exception:
            return {}
    if hasattr(litellm_params, "dict"):
        try:
            return litellm_params.dict()
        except Exception:
            return {}
    return {}

