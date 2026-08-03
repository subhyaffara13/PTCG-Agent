from typing import Any

def build_model_setup(
    model_name: str,
    api_key: str,
    api_base: str,
) -> tuple[str, dict[str, Any]]:
    """Compose ``(model_name, litellm_kwargs)`` for one agent.

    Mirrors :func:`core_harness._setup_model` but takes explicit args so
    callers can pick a model per-agent without touching the global env.
    """
    if api_base and api_base != "dummy_url":
        return f"openai/{model_name}", {
            "api_base": f"{api_base.rstrip('/')}/openapi",
            "api_key": api_key,
            "reasoning_effort": "high",
        }
    if "gemini" in model_name.lower() and not model_name.startswith("gemini/"):
        return f"gemini/{model_name}", {}
    return model_name, {}

