
def anthropic_messages_pt(
    messages: List[AllMessageValues],
    model: str,
    llm_provider: str,
) -> List[
    Union[
        AnthropicMessagesUserMessageParam,
        AnthopicMessagesAssistantMessageParam,
    ]
]:
    """
    format messages for anthropic
    1. Anthropic supports roles like "user" and "assistant" (system prompt sent separately)
    2. The first message always needs to be of role "user"
    3. Each message must alternate between "user" and "assistant" (this is not addressed as now by litellm)
    4. final assistant content cannot end with trailing whitespace (anthropic raises an error otherwise)
    5. System messages are a separate param to the Messages API
    6. Ensure we only accept role, content. (message.name is not supported)
    """
    # Sanitize messages for tool calling issues when modify_params=True
    messages = sanitize_messages_for_tool_calling(messages)

    # Anthropic rejects empty text content blocks with:
    #   "messages: text content blocks must be non-empty"
    # OpenAI/other providers silently tolerate `{"role": "user", "content": ""}`,
    # so callers (and upstream agent frameworks like pydantic-ai) routinely
    # send empty user/assistant turns. We always rewrite these to a placeholder
    # for Anthropic-shaped requests, independent of `litellm.modify_params`,
    # because there is no way to "pass through" an empty text block — the
    # request will always 400 otherwise. The richer tool-call sanitization
    # (Cases A/B/D in `sanitize_messages_for_tool_calling`) remains gated on
    # `modify_params` because it actually mutates conversation structure.
    messages = [_sanitize_empty_text_content(m) for m in messages]

    # add role=tool support to allow function call result/error submission
    user_message_types = {"user", "tool", "function"}
    # reformat messages to ensure user/assistant are alternating, if there's either 2 consecutive 'user' messages or 2 consecutive 'assistant' message, merge them.
    new_messages: List[
        Union[
            AnthropicMessagesUserMessageParam,
            AnthopicMessagesAssistantMessageParam,
        ]
    ] = []

    if len(messages) == 0:
        if not litellm.modify_params:
            raise litellm.BadRequestError(
                message=f"Anthropic requires at least one non-system message. Either provide one, or set `litellm.modify_params = True` // `litellm_settings::modify_params: True` to add the dummy user message - {DEFAULT_USER_CONTINUE_MESSAGE_TYPED}.",
                model=model,
                llm_provider=llm_provider,
            )
        else:
            messages.append(DEFAULT_USER_CONTINUE_MESSAGE_TYPED)

    # Bedrock invoke models have format: invoke/...
    # Vertex AI Anthropic also doesn't support URL sources for images
    is_bedrock_invoke = model.lower().startswith("invoke/")
    is_vertex_ai = llm_provider.startswith("vertex_ai") if llm_provider else False
    force_base64 = is_bedrock_invoke or is_vertex_ai

    msg_i = 0
    while msg_i < len(messages):
        user_content: List[AnthropicMessagesUserMessageValues] = []
        init_msg_i = msg_i
        if isinstance(messages[msg_i], BaseModel):
            messages[msg_i] = dict(messages[msg_i])  # type: ignore
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] in user_message_types:
            user_message_types_block: Union[
                ChatCompletionToolMessage,
                ChatCompletionUserMessage,
                ChatCompletionFunctionMessage,
            ] = messages[
                msg_i
            ]  # type: ignore
            if user_message_types_block["role"] == "user":
                if isinstance(user_message_types_block["content"], list):
                    for m in user_message_types_block["content"]:
                        if m.get("type", "") == "image_url":
                            m = cast(ChatCompletionImageObject, m)
                            format = (
                                m["image_url"].get("format")
                                if isinstance(m["image_url"], dict)
                                else None
                            )
                            # Convert ChatCompletionImageUrlObject to dict if needed
                            image_url_value = m["image_url"]
                            if isinstance(image_url_value, str):
                                image_url_input: Union[str, dict[str, Any]] = (
                                    image_url_value
                                )
                            else:
                                # ChatCompletionImageUrlObject or dict case - convert to dict
                                image_url_input = {
                                    "url": image_url_value["url"],
                                    "format": image_url_value.get("format"),
                                }
                            # Bedrock invoke models have format: invoke/...
                            # Vertex AI Anthropic also doesn't support URL sources for images
                            is_bedrock_invoke = model.lower().startswith("invoke/")
                            is_vertex_ai = (
                                llm_provider.startswith("vertex_ai")
                                if llm_provider
                                else False
                            )
                            force_base64 = is_bedrock_invoke or is_vertex_ai
                            _anthropic_content_element = create_anthropic_image_param(
                                image_url_input,
                                format=format,
                                is_bedrock_invoke=force_base64,
                            )
                            _content_element = add_cache_control_to_content(
                                anthropic_content_element=_anthropic_content_element,
                                original_content_element=dict(m),
                            )

                            if "cache_control" in _content_element:
                                _anthropic_content_element["cache_control"] = (
                                    _content_element["cache_control"]
                                )
                            user_content.append(_anthropic_content_element)
                        elif m.get("type", "") == "text":
                            m = cast(ChatCompletionTextObject, m)
                            _anthropic_text_content_element = (
                                AnthropicMessagesTextParam(
                                    type="text",
                                    text=m["text"],
                                )
                            )
                            _content_element = add_cache_control_to_content(
                                anthropic_content_element=_anthropic_text_content_element,
                                original_content_element=dict(m),
                            )
                            _content_element = cast(
                                AnthropicMessagesTextParam, _content_element
                            )

                            user_content.append(_content_element)
                        elif m.get("type", "") == "document":
                            _document_content_element = cast(
                                AnthropicMessagesDocumentParam,
                                add_cache_control_to_content(
                                    anthropic_content_element=cast(
                                        AnthropicMessagesDocumentParam, m
                                    ),
                                    original_content_element=dict(m),
                                ),
                            )
                            user_content.append(_document_content_element)
                        elif m.get("type", "") == "file":
                            _file_content_element = (
                                anthropic_process_openai_file_message(
                                    cast(ChatCompletionFileObject, m)
                                )
                            )
                            _file_content_element = add_cache_control_to_content(
                                anthropic_content_element=cast(
                                    AnthropicMessagesDocumentParam,
                                    _file_content_element,
                                ),
                                original_content_element=dict(m),
                            )
                            user_content.append(
                                cast(
                                    AnthropicMessagesDocumentParam,
                                    _file_content_element,
                                )
                            )
                elif isinstance(user_message_types_block["content"], str):
                    _anthropic_content_text_element: AnthropicMessagesTextParam = {
                        "type": "text",
                        "text": user_message_types_block["content"],
                    }
                    _content_element = add_cache_control_to_content(
                        anthropic_content_element=_anthropic_content_text_element,
                        original_content_element=dict(user_message_types_block),
                    )

                    if "cache_control" in _content_element:
                        _anthropic_content_text_element["cache_control"] = (
                            _content_element["cache_control"]
                        )

                    user_content.append(_anthropic_content_text_element)

            elif (
                user_message_types_block["role"] == "tool"
                or user_message_types_block["role"] == "function"
            ):
                # OpenAI's tool message content will always be a string
                user_content.append(
                    convert_to_anthropic_tool_result(
                        user_message_types_block, force_base64=force_base64
                    )
                )

            msg_i += 1

        if user_content:
            new_messages.append({"role": "user", "content": user_content})

        # Track unique tool IDs in this merge block to avoid duplication
        unique_tool_ids: Set[str] = set()

        assistant_content: List[AnthropicMessagesAssistantMessageValues] = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            assistant_content_block: ChatCompletionAssistantMessage = messages[msg_i]  # type: ignore

            # Extract compaction_blocks from provider_specific_fields and add them first
            _provider_specific_fields_raw = assistant_content_block.get(
                "provider_specific_fields"
            )
            if isinstance(_provider_specific_fields_raw, dict):
                _compaction_blocks = _provider_specific_fields_raw.get(
                    "compaction_blocks"
                )
                if _compaction_blocks and isinstance(_compaction_blocks, list):
                    # Add compaction blocks at the beginning of assistant content : https://platform.claude.com/docs/en/build-with-claude/compaction
                    assistant_content.extend(_compaction_blocks)  # type: ignore

            thinking_blocks = assistant_content_block.get("thinking_blocks", None)

            # Check if tool_calls contain server tool calls (web search, etc.)
            # If so, we need to interleave thinking blocks with tool call groups
            # to preserve the original content block ordering.
            # Fixes: https://github.com/BerriAI/litellm/issues/23047
            assistant_tool_calls = assistant_content_block.get("tool_calls")
            _has_server_tool_calls = False
            if assistant_tool_calls is not None:
                for _tc in assistant_tool_calls:
                    _tc_id = (
                        _tc.get("id")
                        if isinstance(_tc, dict)
                        else getattr(_tc, "id", None)
                    )
                    if (
                        _tc_id
                        and isinstance(_tc_id, str)
                        and _tc_id.startswith("srvtoolu_")
                    ):
                        _has_server_tool_calls = True
                        break

            if (
                thinking_blocks is not None
                and _has_server_tool_calls
                and isinstance(
                    assistant_content_block.get("content", None), (str, type(None))
                )
            ):
                # INTERLEAVED MODE: When we have both thinking blocks and server
                # tool calls (e.g. web search), Anthropic's original response
                # interleaves them: [thinking_1, server_tool_use_1, result_1,
                # thinking_2, text, server_tool_use_2, result_2, ...].
                # We must preserve this interleaved order because Anthropic
                # verifies thinking block signatures based on position.

                # Build the tool call groups (server_tool_use + its result)
                _provider_specific_fields_raw_tc = assistant_content_block.get(
                    "provider_specific_fields"
                )
                _provider_specific_fields_tc: Dict[str, Any] = {}
                if isinstance(_provider_specific_fields_raw_tc, dict):
                    _provider_specific_fields_tc = cast(
                        Dict[str, Any], _provider_specific_fields_raw_tc
                    )
                _web_search_results_tc = _provider_specific_fields_tc.get(
                    "web_search_results"
                )
                _tool_results_tc = _provider_specific_fields_tc.get("tool_results")
                tool_invoke_results = convert_to_anthropic_tool_invoke(
                    assistant_tool_calls,  # type: ignore
                    web_search_results=_web_search_results_tc,
                    tool_results=_tool_results_tc,
                )

                # Group tool invoke results into (server_tool_use, result) pairs
                # and separate regular tool_use blocks
                server_tool_groups: List[List[Any]] = []
                regular_tool_uses: List[Any] = []
                _current_group: List[Any] = []
                for item in tool_invoke_results:
                    item_type = (
                        item.get("type", "")
                        if isinstance(item, dict)
                        else getattr(item, "type", "")
                    )
                    if item_type == "server_tool_use":
                        if _current_group:
                            server_tool_groups.append(_current_group)
                        _current_group = [item]
                    elif item_type.endswith("_tool_result"):
                        _current_group.append(item)
                    elif item_type == "tool_use":
                        regular_tool_uses.append(item)
                    else:
                        _current_group.append(item)
                if _current_group:
                    server_tool_groups.append(_current_group)

                # Build the text block if content is a non-empty string
                text_element = None
                _acb_content = assistant_content_block.get("content")
                if isinstance(_acb_content, str) and _acb_content:
                    _anthropic_text_content_element = AnthropicMessagesTextParam(
                        type="text",
                        text=_acb_content,
                    )
                    _content_element = add_cache_control_to_content(
                        anthropic_content_element=_anthropic_text_content_element,
                        original_content_element=dict(assistant_content_block),
                    )
                    if "cache_control" in _content_element:
                        _anthropic_text_content_element["cache_control"] = (
                            _content_element["cache_control"]
                        )
                    text_element = _anthropic_text_content_element

                # Interleave: each thinking block precedes its server tool group.
                # Pattern: thinking[0], group[0], thinking[1], group[1], ...
                # Any remaining thinking blocks (after all groups) go before text.
                # Any remaining groups (after all thinking blocks) go after.
                tb_idx = 0
                grp_idx = 0
                num_tb = len(thinking_blocks) if thinking_blocks else 0
                num_grp = len(server_tool_groups)

                while tb_idx < num_tb or grp_idx < num_grp:
                    if tb_idx < num_tb and grp_idx < num_grp:
                        # Emit thinking block then its tool group
                        assistant_content.append(thinking_blocks[tb_idx])
                        tb_idx += 1
                        for block in server_tool_groups[grp_idx]:
                            item_id = (
                                block.get("id")
                                if isinstance(block, dict)
                                else getattr(block, "id", None)
                            )
                            if item_id and item_id in unique_tool_ids:
                                continue
                            if item_id:
                                unique_tool_ids.add(item_id)
                            assistant_content.append(
                                cast(AnthropicMessagesAssistantMessageValues, block)
                            )
                        grp_idx += 1
                    elif tb_idx < num_tb:
                        # More thinking blocks than tool groups - emit before text
                        assistant_content.append(thinking_blocks[tb_idx])
                        tb_idx += 1
                    else:
                        # More tool groups than thinking blocks - emit remaining
                        for block in server_tool_groups[grp_idx]:
                            item_id = (
                                block.get("id")
                                if isinstance(block, dict)
                                else getattr(block, "id", None)
                            )
                            if item_id and item_id in unique_tool_ids:
                                continue
                            if item_id:
                                unique_tool_ids.add(item_id)
                            assistant_content.append(
                                cast(AnthropicMessagesAssistantMessageValues, block)
                            )
                        grp_idx += 1

                # Add text block (if any)
                if text_element is not None:
                    assistant_content.append(text_element)

                # Add regular (non-server) tool calls at the end
                for item in regular_tool_uses:
                    item_id = (
                        item.get("id")
                        if isinstance(item, dict)
                        else getattr(item, "id", None)
                    )
                    if item_id and item_id in unique_tool_ids:
                        continue
                    if item_id:
                        unique_tool_ids.add(item_id)
                    assistant_content.append(
                        cast(AnthropicMessagesAssistantMessageValues, item)
                    )

                # Mark tool_calls as already processed so they are not added again
                assistant_tool_calls = None

            else:
                # SEQUENTIAL MODE: No server tool calls, or no thinking blocks,
                # or content is a list. Use the original sequential approach.

                # When content is a list, check if it already contains thinking
                # blocks inline. If so, skip prepending thinking_blocks to avoid
                # duplication and preserve the original interleaved order.
                # Fixes the gap where list-content messages bypass INTERLEAVED
                # MODE and still get thinking blocks prepended out of order.
                _content_is_list = "content" in assistant_content_block and isinstance(
                    assistant_content_block["content"], list
                )
                _content_list = (
                    assistant_content_block.get("content") if _content_is_list else None
                )
                _list_has_thinking = False
                if _content_is_list and _content_list is not None:
                    for _item in _content_list:
                        if isinstance(_item, dict) and _item.get("type") in (
                            "thinking",
                            "redacted_thinking",
                        ):
                            _list_has_thinking = True
                            break

                if (
                    thinking_blocks is not None and not _list_has_thinking
                ):  # IMPORTANT: ADD THIS FIRST, ELSE ANTHROPIC WILL RAISE AN ERROR
                    assistant_content.extend(thinking_blocks)
                if _content_is_list and _content_list is not None:
                    for m in _content_list:
                        if not isinstance(m, dict):
                            continue
                        # handle thinking blocks
                        thinking_block = cast(str, m.get("thinking", ""))
                        text_block = cast(str, m.get("text", ""))
                        if (
                            m.get("type", "") == "thinking" and len(thinking_block) > 0
                        ):  # don't pass empty text blocks. anthropic api raises errors.
                            anthropic_message: Union[
                                ChatCompletionThinkingBlock,
                                AnthropicMessagesTextParam,
                            ] = cast(ChatCompletionThinkingBlock, m)
                            assistant_content.append(anthropic_message)
                        # handle text
                        elif (
                            m.get("type", "") == "text" and len(text_block) > 0
                        ):  # don't pass empty text blocks. anthropic api raises errors.
                            anthropic_message = AnthropicMessagesTextParam(
                                type="text", text=text_block
                            )
                            _cached_message = add_cache_control_to_content(
                                anthropic_content_element=anthropic_message,
                                original_content_element=dict(m),
                            )

                            assistant_content.append(
                                cast(AnthropicMessagesTextParam, _cached_message)
                            )
                        # handle server_tool_use blocks (tool search, web search, etc.)
                        # Pass through as-is since these are Anthropic-native content types
                        elif m.get("type", "") == "server_tool_use":
                            assistant_content.append(m)  # type: ignore
                        # handle all *_tool_result blocks (tool_search_tool_result,
                        # web_search_tool_result, bash_code_execution_tool_result, etc.)
                        # Pass through as-is since these are Anthropic-native content types
                        elif m.get("type", "").endswith("_tool_result"):
                            assistant_content.append(m)  # type: ignore
                elif (
                    "content" in assistant_content_block
                    and isinstance(assistant_content_block["content"], str)
                    and assistant_content_block[
                        "content"
                    ]  # don't pass empty text blocks. anthropic api raises errors.
                ):
                    _anthropic_text_content_element = AnthropicMessagesTextParam(
                        type="text",
                        text=assistant_content_block["content"],
                    )

                    _content_element = add_cache_control_to_content(
                        anthropic_content_element=_anthropic_text_content_element,
                        original_content_element=dict(assistant_content_block),
                    )

                    if "cache_control" in _content_element:
                        _anthropic_text_content_element["cache_control"] = (
                            _content_element["cache_control"]
                        )

                    assistant_content.append(_anthropic_text_content_element)

            if (
                assistant_tool_calls is not None
            ):  # support assistant tool invoke conversion
                # Get web_search_results and tool_results from provider_specific_fields
                # for server_tool_use reconstruction.
                # Fixes: https://github.com/BerriAI/litellm/issues/17737
                _provider_specific_fields_raw = assistant_content_block.get(
                    "provider_specific_fields"
                )
                _provider_specific_fields: Dict[str, Any] = {}
                if isinstance(_provider_specific_fields_raw, dict):
                    _provider_specific_fields = cast(
                        Dict[str, Any], _provider_specific_fields_raw
                    )
                _web_search_results = _provider_specific_fields.get(
                    "web_search_results"
                )
                _tool_results = _provider_specific_fields.get("tool_results")
                tool_invoke_results = convert_to_anthropic_tool_invoke(
                    assistant_tool_calls,
                    web_search_results=_web_search_results,
                    tool_results=_tool_results,
                )

                # Prevent "tool_use ids must be unique" errors by filtering duplicates
                # This can happen when merging history that already contains the tool calls
                for item in tool_invoke_results:
                    # tool_use items are typically dicts, but handle objects just in case
                    item_id = (
                        item.get("id")
                        if isinstance(item, dict)
                        else getattr(item, "id", None)
                    )

                    if item_id:
                        if item_id in unique_tool_ids:
                            continue
                        unique_tool_ids.add(item_id)

                    assistant_content.append(
                        cast(AnthropicMessagesAssistantMessageValues, item)
                    )

            assistant_function_call = assistant_content_block.get("function_call")

            if assistant_function_call is not None:
                assistant_content.extend(
                    convert_function_to_anthropic_tool_invoke(assistant_function_call)
                )

            msg_i += 1

        if assistant_content:
            new_messages.append({"role": "assistant", "content": assistant_content})

        if msg_i == init_msg_i:  # prevent infinite loops
            raise litellm.BadRequestError(
                message=BAD_MESSAGE_ERROR_STR + f"passed in {messages[msg_i]}",
                model=model,
                llm_provider=llm_provider,
            )

    if len(new_messages) > 0 and new_messages[-1]["role"] == "assistant":
        if isinstance(new_messages[-1]["content"], str):
            new_messages[-1]["content"] = new_messages[-1]["content"].rstrip()
        elif isinstance(new_messages[-1]["content"], list):
            for content in new_messages[-1]["content"]:
                if isinstance(content, dict) and content["type"] == "text":
                    content["text"] = content[
                        "text"
                    ].rstrip()  # no trailing whitespace for final assistant message

    return new_messages

