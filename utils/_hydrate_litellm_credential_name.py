from typing import Optional

def _hydrate_litellm_credential_name(
    litellm_params: Optional[LiteLLM_Params],
) -> Optional[LiteLLM_Params]:
    if litellm_params is None or litellm_params.litellm_credential_name is None:
        return litellm_params

    credential_values = CredentialAccessor.get_credential_values(
        litellm_params.litellm_credential_name
    )
    if not credential_values:
        return litellm_params

    litellm_params = litellm_params.model_copy()
    for key, value in credential_values.items():
        if (
            key in _CREDENTIAL_LITELLM_PARAM_FIELDS
            and getattr(litellm_params, key, None) is None
        ):
            setattr(litellm_params, key, value)
    litellm_params.litellm_credential_name = None
    return litellm_params

