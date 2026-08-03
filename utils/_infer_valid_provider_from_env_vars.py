import os
from typing import List, Optional

def _infer_valid_provider_from_env_vars(
    custom_llm_provider: Optional[str] = None,
) -> List[str]:
    valid_providers: List[str] = []
    environ_keys = os.environ.keys()
    for provider in litellm.provider_list:
        if custom_llm_provider and provider != custom_llm_provider:
            continue

        # edge case litellm has together_ai as a provider, it should be togetherai
        env_provider_1 = provider.replace("_", "")
        env_provider_2 = provider

        # litellm standardizes expected provider keys to
        # PROVIDER_API_KEY. Example: OPENAI_API_KEY, COHERE_API_KEY
        expected_provider_key_1 = f"{env_provider_1.upper()}_API_KEY"
        expected_provider_key_2 = f"{env_provider_2.upper()}_API_KEY"
        if (
            expected_provider_key_1 in environ_keys
            or expected_provider_key_2 in environ_keys
        ):
            # key is set
            valid_providers.append(provider)

    return valid_providers

