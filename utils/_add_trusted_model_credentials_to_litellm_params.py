from typing import Any, Dict

def _add_trusted_model_credentials_to_litellm_params(
    litellm_params_dict: Dict[str, Any], kwargs: Dict[str, Any]
) -> None:
    trusted_model_credentials = kwargs.get("_litellm_internal_model_credentials")
    if isinstance(trusted_model_credentials, type(MappingProxyType({}))):
        litellm_params_dict["_litellm_internal_model_credentials"] = (
            trusted_model_credentials
        )

