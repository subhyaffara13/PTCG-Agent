
def _setup_model() -> tuple[str, dict[str, Any]]:
    """Read env vars and return ``(model_name, litellm_kwargs)``."""
    if "MODEL_NAME" not in os.environ:
        raise ValueError("MODEL_NAME environment variable is required.")
    if "MODEL_PROXY_KEY" not in os.environ:
        raise ValueError("MODEL_PROXY_KEY environment variable is required.")
    if "MODEL_PROXY_URL" not in os.environ:
        raise ValueError("MODEL_PROXY_URL environment variable is required.")

    model_name: str = os.environ["MODEL_NAME"]
    litellm_kwargs: dict[str, Any] = {}

    if os.environ["MODEL_PROXY_URL"] != "dummy_url":
        model_name = f"openai/{model_name}"
        litellm_kwargs = {
            "api_base": f"{os.environ['MODEL_PROXY_URL']}/openapi",
            "api_key": os.environ["MODEL_PROXY_KEY"],
            "reasoning_effort": "high",
        }
    elif "gemini" in model_name.lower() and not model_name.startswith("gemini/"):
        model_name = f"gemini/{model_name}"

    return model_name, litellm_kwargs

