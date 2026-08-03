import os

def _get_extended_environ() -> dict[str, str]:
    """Return a copy of ``os.environ`` with the user's HF token injected (if available)."""
    from huggingface_hub import get_token

    extended_environ = os.environ.copy()
    if (token := get_token()) is not None:
        extended_environ["HF_TOKEN"] = token
    return extended_environ

