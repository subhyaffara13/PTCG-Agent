import json
from typing import List, Optional, Union

def convert_to_model_response_object(
    response_object: Optional[dict] = None,
    model_response_object: Optional[
        Union[
            ModelResponse,
            EmbeddingResponse,
            ImageResponse,
            TranscriptionResponse,
            RerankResponse,
        ]
    ] = None,
    response_type: Literal[
        "completion", "embedding", "image_generation", "audio_transcription", "rerank"
    ] = "completion",
    stream=False,
    start_time=None,
    end_time=None,
    hidden_params: Optional[dict] = None,
    _response_headers: Optional[dict] = None,
    convert_tool_call_to_json_mode: Optional[
        bool
    ] = None,  # used for supporting 'json_schema' on older models
):
    additional_headers = get_response_headers(_response_headers)

    if hidden_params is None:
        hidden_params = {}

    # Preserve existing additional_headers if they contain important provider headers
    # For responses API, additional_headers may already be set with LLM provider headers
    existing_additional_headers = hidden_params.get("additional_headers", {})
    if existing_additional_headers and _response_headers is None:
        # Keep existing headers when _response_headers is None (responses API case)
        additional_headers = existing_additional_headers
    else:
        # Merge new headers with existing ones
        if existing_additional_headers:
            additional_headers.update(existing_additional_headers)

    hidden_params["additional_headers"] = additional_headers

    ### CHECK IF ERROR IN RESPONSE ### - openrouter returns these in the dictionary
    # Some OpenAI-compatible providers (e.g., Apertis) return empty error objects
    # even on success. Only raise if the error contains meaningful data.
    if (
        response_object is not None
        and "error" in response_object
        and response_object["error"] is not None
    ):
        error_obj = response_object["error"]
        has_meaningful_error = False

        if isinstance(error_obj, dict):
            # Check if error dict has non-empty message or non-null code
            error_message = error_obj.get("message", "")
            error_code = error_obj.get("code")
            has_meaningful_error = bool(error_message) or error_code is not None
        elif isinstance(error_obj, str):
            # String error is meaningful if non-empty
            has_meaningful_error = bool(error_obj)
        else:
            # Any other truthy value is considered meaningful
            has_meaningful_error = True

        if has_meaningful_error:
            error_args = {"status_code": 422, "message": "Error in response object"}
            if isinstance(error_obj, dict):
                if "code" in error_obj:
                    error_args["status_code"] = error_obj["code"]
                if "message" in error_obj:
                    if isinstance(error_obj["message"], dict):
                        message_str = json.dumps(error_obj["message"])
                    else:
                        message_str = str(error_obj["message"])
                    error_args["message"] = message_str
            raised_exception = Exception()
            setattr(raised_exception, "status_code", error_args["status_code"])
            setattr(raised_exception, "message", error_args["message"])
            raise raised_exception

    try:
        if response_type == "completion" and (
            model_response_object is None
            or isinstance(model_response_object, ModelResponse)
        ):
            if response_object is None or model_response_object is None:
                raise Exception("Error in response object format")
            if stream is True:
                # for returning cached responses, we need to yield a generator
                return convert_to_streaming_response(response_object=response_object)
            choice_list: List[Choices] = []

            if not response_object.get("choices") or not isinstance(
                response_object["choices"], Iterable
            ):
                from litellm.exceptions import APIError

                raise APIError(
                    status_code=500,
                    message=(
                        "LiteLLM: provider returned a response with no 'choices'. "
                        f"Raw keys: {list(response_object.keys())}"
                    ),
                    llm_provider="",
                    model="",
                )

            for idx, choice in enumerate(response_object["choices"]):
                ## HANDLE JSON MODE - anthropic returns single function call]
                tool_calls = choice["message"].get("tool_calls", None)
                if tool_calls is not None:
                    _openai_tool_calls = []
                    for _tc in tool_calls:
                        _openai_tc = ChatCompletionMessageToolCall(**_tc)
                        _openai_tool_calls.append(_openai_tc)
                    fixed_tool_calls = _handle_invalid_parallel_tool_calls(
                        _openai_tool_calls
                    )

                    if fixed_tool_calls is not None:
                        tool_calls = fixed_tool_calls

                message: Optional[Message] = None
                finish_reason: Optional[str] = None
                if _should_convert_tool_call_to_json_mode(
                    tool_calls=tool_calls,
                    convert_tool_call_to_json_mode=convert_tool_call_to_json_mode,
                ):
                    # to support 'json_schema' logic on older models
                    json_mode_content_str: Optional[str] = tool_calls[0][
                        "function"
                    ].get("arguments")
                    if json_mode_content_str is not None:
                        message = litellm.Message(content=json_mode_content_str)
                        finish_reason = "stop"
                if message is None:
                    # Preserve provider_specific_fields if already present
                    # in the response (e.g. from proxy passthrough)
                    provider_specific_fields = dict(
                        choice["message"].get("provider_specific_fields", None) or {}
                    )
                    for f in choice["message"].keys() - _MESSAGE_FIELDS:
                        provider_specific_fields[f] = choice["message"][f]

                    # Handle reasoning models that display `reasoning_content` within `content`
                    reasoning_content, content = _extract_reasoning_content(
                        choice["message"]
                    )

                    # Handle thinking models that display `thinking_blocks` within `content`
                    thinking_blocks: Optional[
                        List[
                            Union[
                                ChatCompletionThinkingBlock,
                                ChatCompletionRedactedThinkingBlock,
                            ]
                        ]
                    ] = None
                    if "thinking_blocks" in choice["message"]:
                        thinking_blocks = choice["message"]["thinking_blocks"]
                        provider_specific_fields["thinking_blocks"] = thinking_blocks

                    message = Message(
                        content=content,
                        role=choice["message"]["role"] or "assistant",
                        function_call=choice["message"].get("function_call", None),
                        tool_calls=tool_calls,
                        audio=choice["message"].get("audio", None),
                        provider_specific_fields=provider_specific_fields,
                        reasoning_content=reasoning_content,
                        thinking_blocks=thinking_blocks,
                        annotations=choice["message"].get("annotations", None),
                        images=_normalize_images_for_message(
                            choice["message"].get("images", None)
                        ),
                    )
                    finish_reason = choice.get("finish_reason", None)
                if finish_reason is None:
                    # gpt-4 vision can return 'finish_reason' or 'finish_details'
                    finish_reason = choice.get("finish_details") or "stop"
                if (
                    finish_reason == "stop"
                    and message.tool_calls
                    and len(message.tool_calls) > 0
                ):
                    finish_reason = "tool_calls"

                ## PROVIDER SPECIFIC FIELDS ##
                provider_specific_fields = {
                    f: choice[f] for f in choice.keys() - _CHOICES_FIELDS
                }

                logprobs = choice.get("logprobs", None)
                enhancements = choice.get("enhancements", None)
                choice = Choices(
                    finish_reason=finish_reason,
                    index=idx,
                    message=message,
                    logprobs=logprobs,
                    enhancements=enhancements,
                    provider_specific_fields=provider_specific_fields,
                )
                choice_list.append(choice)
            model_response_object.choices = choice_list  # type: ignore

            if "usage" in response_object and response_object["usage"] is not None:
                usage_object = litellm.Usage(**response_object["usage"])
                setattr(model_response_object, "usage", usage_object)
            if "created" in response_object:
                model_response_object.created = _safe_convert_created_field(
                    response_object["created"]
                )

            if "id" in response_object:
                # Preserve the auto-generated id from ModelResponse.__init__
                # when the provider returns a falsy id (None, "")
                model_response_object.id = (
                    response_object["id"] or model_response_object.id
                )

            if "system_fingerprint" in response_object:
                model_response_object.system_fingerprint = response_object[
                    "system_fingerprint"
                ]

            if "model" in response_object:
                if model_response_object.model is None:
                    model_response_object.model = response_object["model"]
                elif (
                    "/" in model_response_object.model
                    and response_object["model"] is not None
                ):
                    openai_compatible_provider = model_response_object.model.split("/")[
                        0
                    ]
                    model_response_object.model = (
                        openai_compatible_provider + "/" + response_object["model"]
                    )

            if start_time is not None and end_time is not None:
                if isinstance(start_time, type(end_time)):
                    model_response_object._response_ms = (  # type: ignore
                        end_time - start_time
                    ).total_seconds() * 1000

            if hidden_params is not None:
                if model_response_object._hidden_params is None:
                    model_response_object._hidden_params = {}
                model_response_object._hidden_params.update(hidden_params)

            if _response_headers is not None:
                model_response_object._response_headers = _response_headers

            for k, v in response_object.items():
                if k not in _MODEL_RESPONSE_FIELDS:
                    setattr(model_response_object, k, v)

            return model_response_object
        elif response_type == "embedding" and (
            model_response_object is None
            or isinstance(model_response_object, EmbeddingResponse)
        ):
            if response_object is None:
                raise Exception("Error in response object format")

            if model_response_object is None:
                model_response_object = EmbeddingResponse()

            if "model" in response_object:
                model_response_object.model = response_object["model"]

            if "object" in response_object:
                model_response_object.object = response_object["object"]

            model_response_object.data = response_object["data"]

            if "usage" in response_object and response_object["usage"] is not None:
                model_response_object.usage.completion_tokens = response_object["usage"].get("completion_tokens", 0)  # type: ignore
                model_response_object.usage.prompt_tokens = response_object["usage"].get("prompt_tokens", 0)  # type: ignore
                model_response_object.usage.total_tokens = response_object["usage"].get("total_tokens", 0)  # type: ignore

            if start_time is not None and end_time is not None:
                model_response_object._response_ms = (  # type: ignore
                    end_time - start_time
                ).total_seconds() * 1000  # return response latency in ms like openai

            if hidden_params is not None:
                model_response_object._hidden_params = hidden_params

            if _response_headers is not None:
                model_response_object._response_headers = _response_headers

            return model_response_object
        elif response_type == "image_generation" and (
            model_response_object is None
            or isinstance(model_response_object, ImageResponse)
        ):
            if response_object is None:
                raise Exception("Error in response object format")

            return LiteLLMResponseObjectHandler.convert_to_image_response(
                response_object=response_object,
                model_response_object=model_response_object,
                hidden_params=hidden_params,
            )

        elif response_type == "audio_transcription" and (
            model_response_object is None
            or isinstance(model_response_object, TranscriptionResponse)
        ):
            if response_object is None:
                raise Exception("Error in response object format")

            if model_response_object is None:
                model_response_object = TranscriptionResponse()

            if "text" in response_object:
                model_response_object.text = response_object["text"]

            optional_keys = ["language", "task", "duration", "words", "segments"]
            for key in optional_keys:  # not guaranteed to be in response
                if key in response_object:
                    setattr(model_response_object, key, response_object[key])

            if "usage" in response_object and response_object["usage"] is not None:
                tr_usage_object: Optional[
                    Union[
                        TranscriptionUsageDurationObject, TranscriptionUsageTokensObject
                    ]
                ] = None

                if response_object["usage"].get("type", None) == "duration":
                    tr_usage_object = TranscriptionUsageDurationObject(
                        **response_object["usage"]
                    )
                elif response_object["usage"].get("type", None) == "tokens":
                    tr_usage_object = TranscriptionUsageTokensObject(
                        **response_object["usage"]
                    )
                if tr_usage_object is not None:
                    setattr(model_response_object, "usage", tr_usage_object)

            if hidden_params is not None:
                model_response_object._hidden_params = hidden_params

            # Store internally-calculated duration in _hidden_params for cost
            # tracking without exposing it in the response body. Must be set
            # after hidden_params assignment to avoid being overwritten.
            if "_audio_transcription_duration" in response_object:
                model_response_object._hidden_params["audio_transcription_duration"] = (
                    response_object["_audio_transcription_duration"]
                )

            if _response_headers is not None:
                model_response_object._response_headers = _response_headers

            return model_response_object
        elif response_type == "rerank" and (
            model_response_object is None
            or isinstance(model_response_object, RerankResponse)
        ):
            if response_object is None:
                raise Exception("Error in response object format")

            if model_response_object is None:
                model_response_object = RerankResponse(**response_object)
                return model_response_object

            if "id" in response_object:
                model_response_object.id = response_object["id"]

            if "meta" in response_object:
                model_response_object.meta = response_object["meta"]

            if "results" in response_object:
                model_response_object.results = response_object["results"]

            return model_response_object
    except Exception as e:
        from litellm.exceptions import APIError

        if isinstance(e, APIError):
            raise

        received_args = dict(
            response_object=response_object,
            model_response_object=model_response_object,
            response_type=response_type,
            stream=stream,
            start_time=start_time,
            end_time=end_time,
            convert_tool_call_to_json_mode=convert_tool_call_to_json_mode,
        )
        raise Exception(
            f"Invalid response object {traceback.format_exc()}\n\nreceived_args={received_args}"
        )

