from typing import Any, Union

def _resolve_fine_tuning_timeout(
    timeout: Any,
    custom_llm_provider: str,
) -> Union[float, httpx.Timeout]:
    """Normalise a raw timeout value to a float (seconds) or httpx.Timeout for fine-tuning calls."""
    timeout = timeout or 600.0
    if isinstance(timeout, httpx.Timeout):
        if not supports_httpx_timeout(custom_llm_provider):
            return float(timeout.read or 600)
        return timeout
    return float(timeout)

