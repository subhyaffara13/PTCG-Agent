import sys
from typing import Optional

def _get_potential_model_names(
    model: str, custom_llm_provider: Optional[str]
) -> PotentialModelNamesAndCustomLLMProvider:
    if custom_llm_provider is None:
        # Get custom_llm_provider
        try:
            get_llm_provider = getattr(sys.modules[__name__], "get_llm_provider")
            split_model, custom_llm_provider, _, _ = get_llm_provider(model=model)
        except Exception:
            split_model = model
        combined_model_name = model
        stripped_model_name = _strip_model_name(
            model=model, custom_llm_provider=custom_llm_provider
        )
        combined_stripped_model_name = stripped_model_name
    elif custom_llm_provider and model.startswith(
        custom_llm_provider + "/"
    ):  # handle case where custom_llm_provider is provided and model starts with custom_llm_provider
        split_model = model.split("/", 1)[1]
        combined_model_name = model
        stripped_model_name = _strip_model_name(
            model=split_model, custom_llm_provider=custom_llm_provider
        )
        combined_stripped_model_name = "{}/{}".format(
            custom_llm_provider, stripped_model_name
        )
    else:
        split_model = model
        combined_model_name = "{}/{}".format(custom_llm_provider, model)
        stripped_model_name = _strip_model_name(
            model=model, custom_llm_provider=custom_llm_provider
        )
        combined_stripped_model_name = "{}/{}".format(
            custom_llm_provider,
            stripped_model_name,
        )

    return PotentialModelNamesAndCustomLLMProvider(
        split_model=split_model,
        combined_model_name=combined_model_name,
        stripped_model_name=stripped_model_name,
        combined_stripped_model_name=combined_stripped_model_name,
        custom_llm_provider=cast(str, custom_llm_provider),
    )

