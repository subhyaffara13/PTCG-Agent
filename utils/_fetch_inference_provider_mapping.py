import os

def _fetch_inference_provider_mapping(model: str) -> dict:
    """
    Fetch provider mappings for a model from the Hugging Face Hub.

    Args:
        model: The model identifier (e.g., 'meta-llama/Llama-2-7b')

    Returns:
        dict: The inference provider mapping for the model

    Raises:
        ValueError: If no provider mapping is found
        HuggingFaceError: If the API request fails
    """
    headers = {"Accept": "application/json"}
    if os.getenv("HUGGINGFACE_API_KEY"):
        headers["Authorization"] = f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"

    path = f"{HF_HUB_URL}/api/models/{model}"
    params = {"expand": ["inferenceProviderMapping"]}

    try:
        response = httpx.get(path, headers=headers, params=params)
        response.raise_for_status()
        provider_mapping = response.json().get("inferenceProviderMapping")

        if provider_mapping is None:
            raise ValueError(f"No provider mapping found for model {model}")

        return provider_mapping
    except httpx.HTTPError as e:
        if hasattr(e, "response"):
            status_code = getattr(e.response, "status_code", 500)
            headers = getattr(e.response, "headers", {})
        else:
            status_code = 500
            headers = {}
        raise HuggingFaceError(
            message=f"Failed to fetch provider mapping: {str(e)}",
            status_code=status_code,
            headers=headers,
        )


def _fetch_inference_provider_mapping(model: str) -> list["InferenceProviderMapping"]:
    """
    Fetch provider mappings for a model from the Hub.
    """
    from huggingface_hub.hf_api import HfApi

    info = HfApi().model_info(model, expand=["inferenceProviderMapping"])
    provider_mapping = info.inference_provider_mapping
    if provider_mapping is None:
        raise ValueError(f"No provider mapping found for model {model}")
    return provider_mapping

