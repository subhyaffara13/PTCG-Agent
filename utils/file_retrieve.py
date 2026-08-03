import time
from typing import Dict, Optional

def file_retrieve(
    file_id: str,
    custom_llm_provider: FileRetrieveProvider = "openai",
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    **kwargs,
) -> FileObject:
    """
    Returns the contents of the specified file.

    LiteLLM Equivalent of POST: POST https://api.openai.com/v1/files
    """
    try:
        optional_params = GenericLiteLLMParams(**kwargs)
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

        _is_async = kwargs.pop("is_async", False) is True

        if custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS:
            openai_creds = get_openai_credentials(
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                organization=optional_params.organization,
            )
            response = openai_files_instance.retrieve_file(
                file_id=file_id,
                _is_async=_is_async,
                api_base=openai_creds.api_base,
                api_key=openai_creds.api_key,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                organization=openai_creds.organization,
            )
        elif custom_llm_provider == "azure":
            azure_creds = get_azure_credentials(
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                api_version=optional_params.api_version,
            )
            response = azure_files_instance.retrieve_file(
                _is_async=_is_async,
                api_base=azure_creds.api_base,
                api_key=azure_creds.api_key,
                api_version=azure_creds.api_version,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                file_id=file_id,
            )
        else:
            # Try using provider config pattern (for Manus, Bedrock, etc.)
            provider_config = ProviderConfigManager.get_provider_files_config(
                model="",
                provider=LlmProviders(custom_llm_provider),
            )
            if provider_config is not None:
                litellm_params_dict = get_litellm_params(**kwargs)
                _add_trusted_model_credentials_to_litellm_params(
                    litellm_params_dict=litellm_params_dict,
                    kwargs=kwargs,
                )
                litellm_params_dict["api_key"] = optional_params.api_key
                litellm_params_dict["api_base"] = optional_params.api_base

                logging_obj = kwargs.get("litellm_logging_obj")
                if logging_obj is None:
                    from litellm.litellm_core_utils.litellm_logging import (
                        Logging as LiteLLMLoggingObj,
                    )

                    logging_obj = LiteLLMLoggingObj(
                        model="",
                        messages=[],
                        stream=False,
                        call_type="afile_retrieve" if _is_async else "file_retrieve",
                        start_time=time.time(),
                        litellm_call_id=kwargs.get(
                            "litellm_call_id", str(uuid_module.uuid4())
                        ),
                        function_id=str(kwargs.get("id") or ""),
                    )

                client = kwargs.get("client")
                response = base_llm_http_handler.retrieve_file(
                    file_id=file_id,
                    provider_config=provider_config,
                    litellm_params=litellm_params_dict,
                    headers=extra_headers or {},
                    logging_obj=logging_obj,
                    _is_async=_is_async,
                    client=(
                        client
                        if client is not None
                        and isinstance(client, (HTTPHandler, AsyncHTTPHandler))
                        else None
                    ),
                    timeout=timeout,
                )
            else:
                raise litellm.exceptions.BadRequestError(
                    message="LiteLLM doesn't support {} for 'file_retrieve'. Only 'openai', 'azure', 'manus', and 'anthropic' are supported.".format(
                        custom_llm_provider
                    ),
                    model="n/a",
                    llm_provider=custom_llm_provider,
                    response=httpx.Response(
                        status_code=400,
                        content="Unsupported provider",
                        request=httpx.Request(method="create_thread", url="https://github.com/BerriAI/litellm"),  # type: ignore
                    ),
                )

        return cast(FileObject, response)
    except Exception as e:
        raise e

