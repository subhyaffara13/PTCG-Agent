from typing import Union

def process_response_headers(
    response_headers: Union[httpx.Headers, dict],
    preserve_litellm_internal_headers: bool = False,
) -> dict:
    """
    `preserve_litellm_internal_headers` must only be True when the input is a
    LiteLLM-owned dict (e.g. `_hidden_params["additional_headers"]` that has
    already been through one round of processing).  For raw upstream provider
    headers — whether passed as `httpx.Headers` or a plain dict — it must
    remain False, otherwise a malicious provider returning `x-litellm-*` could
    spoof LiteLLM-internal markers (e.g. `x-litellm-attempted-fallbacks`).

    When the input is an `httpx.Headers` object the flag is always treated as
    False regardless of what the caller requested, because `httpx.Headers` is
    always a raw provider response and can never be LiteLLM-owned.
    """
    from litellm.types.utils import OPENAI_RESPONSE_HEADERS

    # Raw httpx.Headers objects come directly from provider HTTP responses and
    # must never be treated as LiteLLM-owned, regardless of caller intent.
    _preserve = preserve_litellm_internal_headers and isinstance(response_headers, dict)

    openai_headers = {}
    processed_headers = {}
    additional_headers = {}

    for k, v in response_headers.items():
        if k in OPENAI_RESPONSE_HEADERS:  # return openai-compatible headers
            openai_headers[k] = v
        if k.startswith(
            "llm_provider-"
        ):  # return raw provider headers (incl. openai-compatible ones)
            processed_headers[k] = v
        elif _preserve and k.startswith("x-litellm-"):
            # LiteLLM's own internal headers (e.g. x-litellm-attempted-fallbacks,
            # x-litellm-model-group) are not LLM provider headers and must not be
            # prefixed. Downstream consumers (proxy override, callers checking
            # whether a fallback happened) look up the bare key.
            processed_headers[k] = v
        else:
            additional_headers["{}-{}".format("llm_provider", k)] = v

    additional_headers = {
        **openai_headers,
        **processed_headers,
        **additional_headers,
    }
    return additional_headers

