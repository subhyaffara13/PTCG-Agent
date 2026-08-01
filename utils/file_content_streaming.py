
def file_content_streaming(
    *,
    file_id: str,
    model: Optional[str],
    custom_llm_provider: Optional[Union[FileContentProvider, str]],
    extra_headers: Optional[Dict[str, str]],
    extra_body: Optional[Dict[str, str]],
    chunk_size: int,
    optional_params: GenericLiteLLMParams,
    timeout: Union[float, httpx.Timeout],
    logging_obj: Optional[LiteLLMLoggingObj],
    _is_async: bool,
    client: Optional[Any],
) -> Union[FileContentStreamingResult, Coroutine[Any, Any, FileContentStreamingResult]]:
    if logging_obj is not None:
        logging_obj.model = model or ""
        logging_obj.model_call_details["model"] = model or ""
        logging_obj.model_call_details["custom_llm_provider"] = custom_llm_provider

        litellm_params = logging_obj.model_call_details.get("litellm_params", {}) or {}
        if optional_params.api_base is not None:
            litellm_params["api_base"] = optional_params.api_base
        logging_obj.model_call_details["litellm_params"] = litellm_params

    def _wrap_streaming_result(
        response: FileContentStreamingResult,
    ) -> FileContentStreamingResult:
        return FileContentStreamingResult(
            stream_iterator=FileContentStreamingResponse(
                stream_iterator=response.stream_iterator,
                file_id=file_id,
                model=model,
                custom_llm_provider=custom_llm_provider,
                logging_obj=logging_obj,
            ),
            headers=response.headers,
        )

    response: Union[
        FileContentStreamingResult, Coroutine[Any, Any, FileContentStreamingResult]
    ] = FileContentStreamingResult(stream_iterator=iter(()), headers={})
    if custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS:
        openai_creds = get_openai_credentials(
            api_base=optional_params.api_base,
            api_key=optional_params.api_key,
            organization=optional_params.organization,
        )
        response = openai_files_instance.file_content_streaming(
            _is_async=_is_async,
            file_content_request=FileContentRequest(
                file_id=file_id,
                extra_headers=extra_headers,
                extra_body=extra_body,
            ),
            api_base=openai_creds.api_base,
            api_key=openai_creds.api_key,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            organization=openai_creds.organization,
            chunk_size=chunk_size,
            client=client,
        )
    else:
        raise litellm.exceptions.BadRequestError(
            message="LiteLLM doesn't support {} for streaming 'file_content'. Supported providers are {}.".format(
                custom_llm_provider,
                sorted(OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS),
            ),
            model="n/a",
            llm_provider=custom_llm_provider,
            response=httpx.Response(
                status_code=400,
                content="Unsupported provider",
                request=httpx.Request(method="create_thread", url="https://github.com/BerriAI/litellm"),  # type: ignore
            ),
        )

    if asyncio.iscoroutine(response):

        async def _await_and_wrap() -> FileContentStreamingResult:
            return _wrap_streaming_result(await response)

        return _await_and_wrap()

    return _wrap_streaming_result(response)

