
def _gemini_convert_messages_with_history(
    messages: List[AllMessageValues],
    model: Optional[str] = None,
    litellm_params: Optional[dict] = None,
    custom_llm_provider: Optional[str] = None,
) -> List[ContentType]:
    """
    Converts given messages from OpenAI format to Gemini format

    - Parts must be iterable
    - Roles must alternate b/w 'user' and 'model' (same as anthropic -> merge consecutive roles)
    - Please ensure that function response turn comes immediately after a function call turn
    """
    user_message_types = {"user", "system"}
    contents: List[ContentType] = []

    last_message_with_tool_calls = None

    msg_i = 0
    tool_call_responses = []
    vertex_project = None
    vertex_credentials = None
    if litellm_params:
        vertex_project = litellm_params.get("vertex_project") or litellm_params.get(
            "vertex_ai_project"
        )
        vertex_credentials = litellm_params.get(
            "vertex_credentials"
        ) or litellm_params.get("vertex_ai_credentials")

    try:
        while msg_i < len(messages):
            user_content: List[PartType] = []
            init_msg_i = msg_i
            ## MERGE CONSECUTIVE USER CONTENT ##
            while (
                msg_i < len(messages) and messages[msg_i]["role"] in user_message_types
            ):
                _message_content = messages[msg_i].get("content")
                if _message_content is not None and isinstance(_message_content, list):
                    _parts: List[PartType] = []
                    for element_idx, element in enumerate(_message_content):
                        if (
                            element["type"] == "text"
                            and "text" in element
                            and len(element["text"]) > 0
                        ):
                            element = cast(ChatCompletionTextObject, element)
                            _part = PartType(text=element["text"])
                            _parts.append(_part)
                        elif element["type"] == "image_url":
                            element = cast(ChatCompletionImageObject, element)
                            img_element = element
                            format: Optional[str] = None
                            media_resolution_enum: Optional[Dict[str, str]] = None
                            raw_image_url = img_element.get("image_url")
                            if raw_image_url is None:
                                raise litellm.BadRequestError(
                                    message="Invalid message content: element type is 'image_url' but 'image_url' field is missing ",
                                    model=model,
                                    llm_provider="vertex_ai",
                                )
                            if isinstance(raw_image_url, dict):
                                image_url = raw_image_url.get("url")
                                if image_url is None:
                                    raise litellm.BadRequestError(
                                        message="Invalid message content: element type is 'image_url' but 'url' field is missing inside 'image_url' ",
                                        model=model,
                                        llm_provider="vertex_ai",
                                    )
                                # TypedDict does not declare mime_type/content_type;
                                # read via Dict[str, Any] for caller-provided MIME fields.
                                image_url_dict = cast(Dict[str, Any], raw_image_url)
                                format = (
                                    image_url_dict.get("format")
                                    or image_url_dict.get("mime_type")
                                    or image_url_dict.get("content_type")
                                )
                                detail = image_url_dict.get("detail")
                                media_resolution_enum = (
                                    _convert_detail_to_media_resolution_enum(detail)
                                )
                            else:
                                image_url = raw_image_url
                            _part = _process_gemini_media(
                                image_url=image_url,
                                format=format,
                                media_resolution_enum=media_resolution_enum,
                                model=model,
                                vertex_project=vertex_project,
                                vertex_credentials=vertex_credentials,
                            )
                            _parts.append(_part)
                        elif element["type"] == "input_audio":
                            audio_element = cast(ChatCompletionAudioObject, element)
                            audio_data = audio_element["input_audio"].get("data")
                            audio_format = audio_element["input_audio"].get("format")
                            if audio_data is not None and audio_format is not None:
                                audio_format_modified = (
                                    "audio/" + audio_format
                                    if audio_format.startswith("audio/") is False
                                    else audio_format
                                )  # Gemini expects audio/wav, audio/mp3, etc.
                                openai_image_str = (
                                    convert_generic_image_chunk_to_openai_image_obj(
                                        image_chunk=GenericImageParsingChunk(
                                            type="base64",
                                            media_type=audio_format_modified,
                                            data=audio_data,
                                        )
                                    )
                                )
                                _part = _process_gemini_media(
                                    image_url=openai_image_str,
                                    format=audio_format_modified,
                                    model=model,
                                    vertex_project=vertex_project,
                                    vertex_credentials=vertex_credentials,
                                )
                                _parts.append(_part)
                        elif element["type"] == "file":
                            file_element = cast(ChatCompletionFileObject, element)
                            _file_field = file_element.get("file")
                            if _file_field is None:
                                raise litellm.BadRequestError(
                                    message="Content block has type='file' but is missing the required 'file' field",
                                    model=model,
                                    llm_provider="vertex_ai",
                                )
                            # TypedDict does not declare mime_type/content_type;
                            # read via Dict[str, Any] for caller-provided MIME fields.
                            file_dict = cast(Dict[str, Any], _file_field)
                            file_id = file_dict.get("file_id")
                            format = (
                                file_dict.get("format")
                                or file_dict.get("mime_type")
                                or file_dict.get("content_type")
                            )
                            file_data = file_dict.get("file_data")
                            detail = file_dict.get("detail")
                            video_metadata = file_dict.get("video_metadata")
                            passed_file = file_id or file_data
                            if passed_file is None:
                                raise Exception(
                                    "Unknown file type. Please pass in a file_id or file_data"
                                )

                            # Convert detail to media_resolution_enum
                            media_resolution_enum = (
                                _convert_detail_to_media_resolution_enum(detail)
                            )

                            try:
                                _part = _process_gemini_media(
                                    image_url=passed_file,
                                    format=format,
                                    model=model,
                                    media_resolution_enum=media_resolution_enum,
                                    video_metadata=video_metadata,
                                    vertex_project=vertex_project,
                                    vertex_credentials=vertex_credentials,
                                )
                                _parts.append(_part)
                            except litellm.BadRequestError:
                                raise
                            except Exception as e:
                                raise litellm.BadRequestError(
                                    message=(
                                        f"Unable to determine mime type for file: "
                                        f"{file_id or 'provided data'}, set this explicitly "
                                        f"using message[{msg_i}].content[{element_idx}].file.format "
                                        f"(or file.mime_type/content_type). "
                                        f"Original error: {str(e)}"
                                    ),
                                    model=model,
                                    llm_provider="vertex_ai",
                                )
                    user_content.extend(_parts)
                elif _message_content is not None and isinstance(_message_content, str):
                    _part = PartType(text=_message_content)
                    user_content.append(_part)

                msg_i += 1

            if user_content:
                """
                check that user_content has 'text' parameter.
                    - Known Vertex Error: Unable to submit request because it must have a text parameter.
                    - Relevant Issue: https://github.com/BerriAI/litellm/issues/5515
                """
                has_text_in_content = _check_text_in_content(user_content)
                if has_text_in_content is False:
                    verbose_logger.warning(
                        "No text in user content. Adding a blank text to user content, to ensure Gemini doesn't fail the request. Relevant Issue - https://github.com/BerriAI/litellm/issues/5515"
                    )
                    user_content.append(
                        PartType(text=" ")
                    )  # add a blank text, to ensure Gemini doesn't fail the request.
                contents.append(ContentType(role="user", parts=user_content))
            assistant_content = []
            ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
            while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
                if isinstance(messages[msg_i], BaseModel):
                    msg_dict: Union[ChatCompletionAssistantMessage, dict] = messages[msg_i].model_dump()  # type: ignore
                else:
                    msg_dict = messages[msg_i]  # type: ignore
                assistant_msg = ChatCompletionAssistantMessage(**msg_dict)  # type: ignore
                _message_content = assistant_msg.get("content", None)
                reasoning_content = assistant_msg.get("reasoning_content", None)
                thinking_blocks = assistant_msg.get("thinking_blocks")
                if reasoning_content is not None:
                    assistant_content.append(
                        PartType(thought=True, text=reasoning_content)
                    )
                if thinking_blocks is not None:
                    for block in thinking_blocks:
                        if block["type"] == "thinking":
                            block_thinking_str = block.get("thinking")
                            block_signature = block.get("signature")
                            if (
                                block_thinking_str is not None
                                and block_signature is not None
                            ):
                                try:
                                    assistant_content.append(
                                        PartType(
                                            thoughtSignature=block_signature,
                                            **json.loads(block_thinking_str),
                                        )
                                    )
                                except Exception:
                                    assistant_content.append(
                                        PartType(
                                            thoughtSignature=block_signature,
                                            text=block_thinking_str,
                                        )
                                    )
                if _message_content is not None and isinstance(_message_content, list):
                    _parts = []
                    for element in _message_content:
                        if isinstance(element, dict):
                            if element["type"] == "text":
                                _part = PartType(text=element["text"])
                                _parts.append(_part)

                    assistant_content.extend(_parts)
                elif _message_content is not None and isinstance(_message_content, str):
                    assistant_text = _message_content
                    # Check if message has thought_signatures in provider_specific_fields
                    provider_specific_fields = assistant_msg.get(
                        "provider_specific_fields"
                    )
                    thought_signatures = None
                    if provider_specific_fields and isinstance(
                        provider_specific_fields, dict
                    ):
                        thought_signatures = provider_specific_fields.get(
                            "thought_signatures"
                        )

                    # If we have thought signatures, add them to the part
                    if (
                        thought_signatures
                        and isinstance(thought_signatures, list)
                        and len(thought_signatures) > 0
                    ):
                        # Use the first signature for the text part (Gemini expects one signature per part)
                        assistant_content.append(PartType(text=assistant_text, thoughtSignature=thought_signatures[0]))  # type: ignore
                    else:
                        assistant_content.append(PartType(text=assistant_text))  # type: ignore

                ## HANDLE ASSISTANT IMAGES FIELD
                # Process images field if present (for generated images from assistant)
                assistant_images = assistant_msg.get("images")
                if assistant_images is not None and isinstance(assistant_images, list):
                    for image_item in assistant_images:
                        if isinstance(image_item, dict):
                            image_url_obj = image_item.get("image_url")
                            if isinstance(image_url_obj, dict):
                                assistant_image_url = image_url_obj.get("url")
                                format = (
                                    image_url_obj.get("format")
                                    or image_url_obj.get("mime_type")
                                    or image_url_obj.get("content_type")
                                )
                                detail = image_url_obj.get("detail")
                                media_resolution_enum = (
                                    _convert_detail_to_media_resolution_enum(detail)
                                )
                                if assistant_image_url:
                                    _part = _process_gemini_media(
                                        image_url=assistant_image_url,
                                        format=format,
                                        media_resolution_enum=media_resolution_enum,
                                        model=model,
                                        vertex_project=vertex_project,
                                        vertex_credentials=vertex_credentials,
                                    )
                                    assistant_content.append(_part)

                ## HANDLE ASSISTANT FUNCTION CALL
                if (
                    assistant_msg.get("tool_calls", []) is not None
                    or assistant_msg.get("function_call") is not None
                ):  # support assistant tool invoke conversion
                    gemini_tool_call_parts = convert_to_gemini_tool_call_invoke(
                        assistant_msg,
                        model=model,
                        custom_llm_provider=custom_llm_provider,
                    )
                    ## check if gemini_tool_call already exists in assistant_content
                    for gemini_tool_call_part in gemini_tool_call_parts:
                        if not check_if_part_exists_in_parts(
                            assistant_content,
                            gemini_tool_call_part,
                            excluded_keys=["thoughtSignature"],
                        ):
                            assistant_content.append(gemini_tool_call_part)
                    # Only record this as the active tool-call message when it actually
                    # carries tool calls. The `if` guard above is also entered for a
                    # text-only assistant message (`assistant_msg.get("tool_calls", [])
                    # is not None` is True for an empty list), so without this check a
                    # later assistant message with no tool calls would clobber the
                    # reference. The following tool result would then be matched against
                    # an assistant message that has no tool_calls, raising "Missing
                    # corresponding tool call for tool response message".
                    if (
                        assistant_msg.get("tool_calls")
                        or assistant_msg.get("function_call") is not None
                    ):
                        last_message_with_tool_calls = assistant_msg

                ## HANDLE SERVER-SIDE TOOL INVOCATIONS (context circulation)
                _psf = assistant_msg.get("provider_specific_fields")
                if isinstance(_psf, dict):
                    _ss_invocations = _psf.get("server_side_tool_invocations")
                    if isinstance(_ss_invocations, list):
                        for invocation in _ss_invocations:
                            # Re-inject toolCall part
                            tc_part: Dict[str, Any] = {
                                "toolCall": {
                                    "toolType": invocation.get("tool_type"),
                                    "id": invocation.get("id"),
                                    "args": invocation.get("args"),
                                }
                            }
                            if "thought_signature" in invocation:
                                tc_part["thoughtSignature"] = invocation[
                                    "thought_signature"
                                ]
                            assistant_content.append(tc_part)  # type: ignore

                            # Re-inject toolResponse part if response is present
                            if "response" in invocation:
                                tr_dict: Dict[str, Any] = {
                                    "id": invocation.get("id"),
                                    "response": invocation.get("response"),
                                }
                                if invocation.get("tool_type"):
                                    tr_dict["toolType"] = invocation["tool_type"]
                                tr_part: Dict[str, Any] = {"toolResponse": tr_dict}
                                if "thought_signature" in invocation:
                                    tr_part["thoughtSignature"] = invocation[
                                        "thought_signature"
                                    ]
                                assistant_content.append(tr_part)  # type: ignore

                msg_i += 1

            if assistant_content:
                contents.append(ContentType(role="model", parts=assistant_content))

            ## APPEND TOOL CALL MESSAGES ##
            tool_call_message_roles = ["tool", "function"]
            if (
                msg_i < len(messages)
                and messages[msg_i]["role"] in tool_call_message_roles
            ):
                _part = convert_to_gemini_tool_call_result(
                    messages[msg_i],  # type: ignore
                    last_message_with_tool_calls,  # type: ignore
                    model=model,
                    custom_llm_provider=custom_llm_provider,
                )
                msg_i += 1
                # Handle both single part and list of parts (for Computer Use with images)
                if isinstance(_part, list):
                    tool_call_responses.extend(_part)
                else:
                    tool_call_responses.append(_part)
            if msg_i < len(messages) and (
                messages[msg_i]["role"] not in tool_call_message_roles
            ):
                if len(tool_call_responses) > 0:
                    contents.append(ContentType(role="user", parts=tool_call_responses))
                    tool_call_responses = []

            if msg_i == init_msg_i:  # prevent infinite loops
                raise Exception(
                    "Invalid Message passed in - {}. File an issue https://github.com/BerriAI/litellm/issues".format(
                        messages[msg_i]
                    )
                )
        if len(tool_call_responses) > 0:
            contents.append(ContentType(role="user", parts=tool_call_responses))

        if len(contents) == 0:
            verbose_logger.warning("""
                No contents in messages. Contents are required. See
                https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.publishers.models/generateContent#request-body.
                If the original request did not comply to OpenAI API requirements it should have failed by now,
                but LiteLLM does not check for missing messages.
                Setting an empty content to prevent an 400 error.
                Relevant Issue - https://github.com/BerriAI/litellm/issues/9733
                """)
            contents.append(ContentType(role="user", parts=[PartType(text=" ")]))
        return contents
    except Exception as e:
        raise e

