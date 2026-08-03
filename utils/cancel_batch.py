import os
from typing import Any, Dict, Optional, Union

def cancel_batch(
    batch_id: str,
    model: Optional[str] = None,
    custom_llm_provider: Union[Literal["openai", "azure", "vertex_ai"], str] = "openai",
    metadata: Optional[Dict[str, str]] = None,
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    **kwargs,
) -> Union[LiteLLMBatch, Coroutine[Any, Any, LiteLLMBatch]]:
    """
    Cancels a batch.

    LiteLLM Equivalent of POST https://api.openai.com/v1/batches/{batch_id}/cancel
    """
    try:
        try:
            if model is not None:
                _, custom_llm_provider, _, _ = get_llm_provider(
                    model=model,
                    custom_llm_provider=custom_llm_provider,
                )
        except Exception as e:
            verbose_logger.exception(
                f"litellm.batches.main.py::cancel_batch() - Error inferring custom_llm_provider - {str(e)}"
            )
        optional_params = GenericLiteLLMParams(**kwargs)
        litellm_params = get_litellm_params(
            custom_llm_provider=custom_llm_provider,
            **kwargs,
        )
        ### TIMEOUT LOGIC ###
        timeout = optional_params.timeout or kwargs.get("request_timeout", 600) or 600
        # set timeout for 10 minutes by default

        if (
            timeout is not None
            and isinstance(timeout, httpx.Timeout)
            and supports_httpx_timeout(custom_llm_provider) is False
        ):
            read_timeout = timeout.read or 600
            timeout = read_timeout  # default 10 min timeout
        elif timeout is not None and not isinstance(timeout, httpx.Timeout):
            timeout = float(timeout)  # type: ignore
        elif timeout is None:
            timeout = 600.0

        _cancel_batch_request = CancelBatchRequest(
            batch_id=batch_id,
            extra_headers=extra_headers,
            extra_body=extra_body,
        )

        _is_async = kwargs.pop("acancel_batch", False) is True
        api_base: Optional[str] = None
        if custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS:
            api_base = (
                optional_params.api_base
                or litellm.api_base
                or os.getenv("OPENAI_BASE_URL")
                or os.getenv("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )
            organization = (
                optional_params.organization
                or litellm.organization
                or os.getenv("OPENAI_ORGANIZATION", None)
                or None
            )
            api_key = (
                optional_params.api_key
                or litellm.api_key
                or litellm.openai_key
                or os.getenv("OPENAI_API_KEY")
            )

            response = openai_batches_instance.cancel_batch(
                _is_async=_is_async,
                cancel_batch_data=_cancel_batch_request,
                api_base=api_base,
                api_key=api_key,
                organization=organization,
                timeout=timeout,
                max_retries=optional_params.max_retries,
            )
        elif custom_llm_provider == "azure":
            api_base = (
                optional_params.api_base
                or litellm.api_base
                or get_secret_str("AZURE_API_BASE")
            )
            api_version = (
                optional_params.api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
            )

            api_key = (
                optional_params.api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_OPENAI_API_KEY")
                or get_secret_str("AZURE_API_KEY")
            )

            extra_body = optional_params.get("extra_body", {})
            if extra_body is not None:
                extra_body.pop("azure_ad_token", None)
            else:
                get_secret_str("AZURE_AD_TOKEN")  # type: ignore

            response = azure_batches_instance.cancel_batch(
                _is_async=_is_async,
                api_base=api_base,
                api_key=api_key,
                api_version=api_version,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                cancel_batch_data=_cancel_batch_request,
                litellm_params=litellm_params,
            )
        elif custom_llm_provider == "vertex_ai":
            api_base = optional_params.api_base or None
            vertex_ai_project = (
                optional_params.vertex_project
                or litellm.vertex_project
                or get_secret_str("VERTEXAI_PROJECT")
            )
            vertex_ai_location = (
                optional_params.vertex_location
                or litellm.vertex_location
                or get_secret_str("VERTEXAI_LOCATION")
            )
            vertex_credentials = optional_params.vertex_credentials or get_secret_str(
                "VERTEXAI_CREDENTIALS"
            )

            response = vertex_ai_batches_instance.cancel_batch(
                _is_async=_is_async,
                batch_id=batch_id,
                api_base=api_base,
                vertex_project=vertex_ai_project,
                vertex_location=vertex_ai_location,
                vertex_credentials=vertex_credentials,
                timeout=timeout,
                max_retries=optional_params.max_retries,
            )
        else:
            raise litellm.exceptions.BadRequestError(
                message="LiteLLM doesn't support {} for 'cancel_batch'. Only 'openai', 'azure', and 'vertex_ai' are supported.".format(
                    custom_llm_provider
                ),
                model="n/a",
                llm_provider=custom_llm_provider,
                response=httpx.Response(
                    status_code=400,
                    content="Unsupported provider",
                    request=httpx.Request(method="cancel_batch", url="https://github.com/BerriAI/litellm"),  # type: ignore
                ),
            )
        return response
    except Exception as e:
        raise e

