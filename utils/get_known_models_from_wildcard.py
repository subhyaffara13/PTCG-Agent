from typing import List, Optional

def get_known_models_from_wildcard(
    wildcard_model: str, litellm_params: Optional[LiteLLM_Params] = None
) -> List[str]:
    try:
        wildcard_provider_prefix, wildcard_suffix = wildcard_model.split("/", 1)
    except ValueError:  # safely fail
        return []

    # Use provider from litellm_params when available, otherwise from wildcard prefix
    # (e.g., "openai" from "openai/*" - needed for BYOK where wildcard isn't in router)
    if litellm_params is not None:
        try:
            provider = litellm_params.model.split("/", 1)[0]
        except ValueError:
            provider = wildcard_provider_prefix
    else:
        provider = wildcard_provider_prefix

    litellm_params = _hydrate_litellm_credential_name(litellm_params)

    wildcard_models = get_provider_models(
        provider=provider, litellm_params=litellm_params
    )

    if wildcard_models is None:
        return []
    if wildcard_suffix != "*":
        ## CHECK IF PARTIAL FILTER e.g. `gemini-*`
        model_prefix = wildcard_suffix.replace("*", "")

        is_partial_filter = any(
            wc_model.startswith(model_prefix) for wc_model in wildcard_models
        )
        if is_partial_filter:
            filtered_wildcard_models = [
                wc_model
                for wc_model in wildcard_models
                if wc_model.startswith(model_prefix)
            ]
            wildcard_models = filtered_wildcard_models
        else:
            # add model prefix to wildcard models
            wildcard_models = [f"{model_prefix}{model}" for model in wildcard_models]

    known_providers = {provider.value for provider in LlmProviders}
    suffix_appended_wildcard_models = []
    for model in wildcard_models:
        if not model.startswith(wildcard_provider_prefix):
            # `get_provider_models` returns provider-prefixed ids (e.g. "ollama/gemma3:1b").
            # When the wildcard uses a custom prefix (e.g. "ollama_server1/*" to distinguish
            # multiple instances), replace that existing provider prefix instead of stacking
            # both, which would otherwise yield an uncallable "ollama_server1/ollama/gemma3:1b".
            # Only strip the leading segment when it is a known provider, so ids whose first
            # segment is an org rather than a provider (e.g. "meta-llama/Llama-3-8B") keep it.
            leading, sep, model_suffix = model.partition("/")
            if sep and leading in known_providers:
                model = f"{wildcard_provider_prefix}/{model_suffix}"
            else:
                model = f"{wildcard_provider_prefix}/{model}"
        suffix_appended_wildcard_models.append(model)
    return suffix_appended_wildcard_models or []

