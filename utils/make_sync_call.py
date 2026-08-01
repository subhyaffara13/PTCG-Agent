
def make_sync_call(
    client: Optional[HTTPHandler],  # module-level client
    gemini_client: Optional[HTTPHandler],  # if passed by user
    api_base: str,
    headers: dict,
    data: str,
    model: str,
    messages: list,
    logging_obj,
):
    if gemini_client is not None:
        client = gemini_client
    if client is None:
        client = HTTPHandler()  # Create a new client if none provided

    response = client.post(
        api_base, headers=headers, data=data, stream=True, logging_obj=logging_obj
    )

    if response.status_code != 200 and response.status_code != 201:
        raise VertexAIError(
            status_code=response.status_code,
            message=str(response.read()),
            headers=response.headers,
        )

    completion_stream = ModelResponseIterator(
        streaming_response=response.iter_lines(),
        sync_stream=True,
        logging_obj=logging_obj,
        response_headers=response.headers,
        response=response,
    )

    # LOGGING
    logging_obj.post_call(
        input=messages,
        api_key="",
        original_response="first stream response received",
        additional_args={"complete_input_dict": data},
    )

    return completion_stream


def make_sync_call(
    client: Optional[HTTPHandler],
    api_base: str,
    headers: dict,
    data: str,
    model: str,
    messages: list,
    logging_obj,
    streaming_decoder: Optional[CustomStreamingDecoder] = None,
    fake_stream: bool = False,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
):
    if client is None:
        client = litellm.module_level_client  # Create a new client if none provided

    response = client.post(
        api_base, headers=headers, data=data, stream=not fake_stream, timeout=timeout
    )

    if response.status_code != 200:
        raise OpenAILikeError(status_code=response.status_code, message=response.read())

    if streaming_decoder is not None:
        completion_stream = streaming_decoder.iter_bytes(
            response.iter_bytes(chunk_size=1024)
        )
    elif fake_stream:
        model_response = ModelResponse(**response.json())
        completion_stream = MockResponseIterator(model_response=model_response)
    else:
        completion_stream = ModelResponseIterator(
            streaming_response=response.iter_lines(), sync_stream=True
        )

    # LOGGING
    logging_obj.post_call(
        input=messages,
        api_key="",
        original_response="first stream response received",
        additional_args={"complete_input_dict": data},
    )

    return completion_stream


def make_sync_call(
    client: Optional[HTTPHandler],
    api_base: str,
    headers: dict,
    data: str,
    model: str,
    messages: list,
    logging_obj: LiteLLMLoggingObject,
    json_mode: Optional[bool] = False,
    fake_stream: bool = False,
    stream_chunk_size: Optional[int] = None,
):
    if client is None:
        client = _get_httpx_client()  # Create a new client if none provided

    response = client.post(
        api_base,
        headers=headers,
        data=data,
        stream=not fake_stream,
        logging_obj=logging_obj,
    )

    if response.status_code != 200:
        raise BedrockError(
            status_code=response.status_code, message=str(response.read())
        )

    if fake_stream:
        model_response: (
            ModelResponse
        ) = litellm.AmazonConverseConfig()._transform_response(
            model=model,
            response=response,
            model_response=litellm.ModelResponse(),
            stream=True,
            logging_obj=logging_obj,
            optional_params={},
            api_key="",
            data=data,
            messages=messages,
            encoding=litellm.encoding,
        )  # type: ignore
        completion_stream: Any = MockResponseIterator(
            model_response=model_response, json_mode=json_mode
        )
    else:
        decoder = AWSEventStreamDecoder(model=model, json_mode=json_mode)
        completion_stream = decoder.iter_bytes(
            response.iter_bytes(chunk_size=stream_chunk_size)
        )

    # LOGGING
    logging_obj.post_call(
        input=messages,
        api_key="",
        original_response="first stream response received",
        additional_args={"complete_input_dict": data},
    )

    return completion_stream


def make_sync_call(
    client: Optional[HTTPHandler],
    api_base: str,
    headers: dict,
    data: str,
    signed_json_body: Optional[bytes],
    model: str,
    messages: list,
    logging_obj: Logging,
    fake_stream: bool = False,
    json_mode: Optional[bool] = False,
    bedrock_invoke_provider: Optional[litellm.BEDROCK_INVOKE_PROVIDERS_LITERAL] = None,
    stream_chunk_size: Optional[int] = None,
):
    try:
        if client is None:
            client = _get_httpx_client(
                params=(
                    {"ssl_verify": logging_obj.litellm_params.get("ssl_verify")}
                    if logging_obj
                    and logging_obj.litellm_params
                    and logging_obj.litellm_params.get("ssl_verify")
                    else None
                )
            )

        response = client.post(
            api_base,
            headers=headers,
            data=signed_json_body if signed_json_body is not None else data,
            stream=not fake_stream,
            logging_obj=logging_obj,
        )

        if response.status_code != 200:
            raise BedrockError(status_code=response.status_code, message=response.text)

        if fake_stream:
            model_response: (
                ModelResponse
            ) = litellm.AmazonConverseConfig()._transform_response(
                model=model,
                response=response,
                model_response=litellm.ModelResponse(),
                stream=True,
                logging_obj=logging_obj,
                optional_params={},
                api_key="",
                data=data,
                messages=messages,
                encoding=litellm.encoding,
            )  # type: ignore
            completion_stream: Any = MockResponseIterator(
                model_response=model_response, json_mode=json_mode
            )
        elif bedrock_invoke_provider == "anthropic":
            decoder: AWSEventStreamDecoder = AmazonAnthropicClaudeStreamDecoder(
                model=model,
                sync_stream=True,
                json_mode=json_mode,
            )
            completion_stream = decoder.iter_bytes(
                response.iter_bytes(chunk_size=stream_chunk_size)
            )
        elif bedrock_invoke_provider == "deepseek_r1":
            decoder = AmazonDeepSeekR1StreamDecoder(
                model=model,
                sync_stream=True,
            )
            completion_stream = decoder.iter_bytes(
                response.iter_bytes(chunk_size=stream_chunk_size)
            )
        else:
            decoder = AWSEventStreamDecoder(model=model, json_mode=json_mode)
            completion_stream = decoder.iter_bytes(
                response.iter_bytes(chunk_size=stream_chunk_size)
            )

        # LOGGING
        logging_obj.post_call(
            input=messages,
            api_key="",
            original_response="first stream response received",
            additional_args={"complete_input_dict": data},
        )

        return completion_stream
    except httpx.HTTPStatusError as err:
        error_code = err.response.status_code
        raise BedrockError(status_code=error_code, message=err.response.text)
    except httpx.TimeoutException:
        raise BedrockError(status_code=408, message="Timeout error occurred.")
    except Exception as e:
        raise BedrockError(status_code=500, message=str(e))


def make_sync_call(
    client: Optional[HTTPHandler],
    api_base: str,
    headers: dict,
    data: str,
    model: str,
    messages: list,
    logging_obj,
    timeout: Optional[Union[float, httpx.Timeout]],
    json_mode: bool,
    speed: Optional[str] = None,
    tool_name_reverse_map: Optional[Dict[str, str]] = None,
) -> Tuple[Any, httpx.Headers]:
    if client is None:
        client = litellm.module_level_client  # re-use a module level client

    try:
        response = client.post(
            api_base,
            headers=headers,
            data=data,
            stream=True,
            timeout=timeout,
            logging_obj=logging_obj,
        )
    except httpx.HTTPStatusError as e:
        error_headers = getattr(e, "headers", None)
        error_response = getattr(e, "response", None)
        if error_headers is None and error_response:
            error_headers = getattr(error_response, "headers", None)
        raise AnthropicError(
            status_code=e.response.status_code,
            message=e.response.read(),
            headers=error_headers,
        )
    except Exception as e:
        for exception in litellm.LITELLM_EXCEPTION_TYPES:
            if isinstance(e, exception):
                raise e
        raise AnthropicError(status_code=500, message=str(e))

    if response.status_code != 200:
        response_headers = getattr(response, "headers", None)
        raise AnthropicError(
            status_code=response.status_code,
            message=response.read(),
            headers=response_headers,
        )

    completion_stream = ModelResponseIterator(
        streaming_response=response.iter_lines(),
        sync_stream=True,
        json_mode=json_mode,
        speed=speed,
        tool_name_reverse_map=tool_name_reverse_map,
    )

    # LOGGING
    logging_obj.post_call(
        input=messages,
        api_key="",
        original_response="first stream response received",
        additional_args={"complete_input_dict": data},
    )

    return completion_stream, response.headers

