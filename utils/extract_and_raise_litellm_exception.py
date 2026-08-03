import re
from typing import Any, Optional

def extract_and_raise_litellm_exception(
    response: Optional[Any],
    error_str: str,
    model: str,
    custom_llm_provider: str,
):
    """
    Covers scenario where litellm sdk calling proxy.

    Enables raising the special errors raised by litellm, eg. ContextWindowExceededError.

    Relevant Issue: https://github.com/BerriAI/litellm/issues/7259
    """
    pattern = r"litellm\.\w+Error"

    # Search for the exception in the error string
    match = re.search(pattern, error_str)

    # Extract the exception if found
    if match:
        exception_name = match.group(0)
        exception_name = exception_name.strip().replace("litellm.", "")
        raised_exception_obj = getattr(litellm, exception_name, None)
        if raised_exception_obj:
            # Try with response parameter first, fall back to without it
            # Some exceptions (e.g., APIConnectionError) don't accept response param
            try:
                raise raised_exception_obj(
                    message=error_str,
                    llm_provider=custom_llm_provider,
                    model=model,
                    response=response,
                )
            except TypeError:
                # Exception doesn't accept response parameter
                raise raised_exception_obj(
                    message=error_str,
                    llm_provider=custom_llm_provider,
                    model=model,
                )

