import os

def _set_env_defaults(model_override: str | None) -> None:
    if model_override is not None:
        os.environ["MODEL_NAME"] = model_override
    elif "MODEL_NAME" not in os.environ:
        os.environ["MODEL_NAME"] = _DEFAULT_MODEL
    if "MODEL_PROXY_KEY" not in os.environ:
        os.environ["MODEL_PROXY_KEY"] = os.environ.get(
            "GEMINI_API_KEY", os.environ.get("OPENAI_API_KEY", "dummy")
        )
    if "MODEL_PROXY_URL" not in os.environ:
        os.environ["MODEL_PROXY_URL"] = "dummy_url"

