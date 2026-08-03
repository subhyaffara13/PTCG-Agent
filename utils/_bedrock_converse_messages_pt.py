from typing import List, Optional, Union

def _bedrock_converse_messages_pt(
    messages: List,
    model: str,
    llm_provider: str,
    user_continue_message: Optional[ChatCompletionUserMessage] = None,
    assistant_continue_message: Optional[
        Union[str, ChatCompletionAssistantMessage]
    ] = None,
) -> List[BedrockMessageBlock]:
    """
    Converts given messages from OpenAI format to Bedrock format

    - Roles must alternate b/w 'user' and 'model' (same as anthropic -> merge consecutive roles)
    - Please ensure that function response turn comes immediately after a function call turn
    - Conversation blocks and tool result blocks cannot be provided in the same turn. Issue: https://github.com/BerriAI/litellm/issues/6053
    """

    contents: List[BedrockMessageBlock] = []
    msg_i = 0

    messages = BedrockConverseMessagesProcessor._initial_message_setup(
        messages, model, llm_provider, user_continue_message
    )

    while msg_i < len(messages):
        user_content: List[BedrockContentBlock] = []
        init_msg_i = msg_i
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "user":
            message_block = get_user_message_block_or_continue_message(
                message=messages[msg_i],
                user_continue_message=user_continue_message,
            )
            if isinstance(message_block["content"], list):
                _parts: List[BedrockContentBlock] = []
                for element in message_block["content"]:
                    if isinstance(element, dict):
                        if element["type"] == "text":
                            _part = BedrockContentBlock(text=element["text"])
                            _parts.append(_part)
                        elif element["type"] == "guarded_text":
                            # Wrap guarded_text in guardContent block
                            _part = BedrockContentBlock(
                                guardContent={"text": {"text": element["text"]}}
                            )
                            _parts.append(_part)
                        elif element["type"] in ("grounding_source", "query"):
                            # Contextual grounding tags are guardrail metadata; the
                            # model only needs the underlying text, so render them as
                            # plain text on the generate path.
                            _part = BedrockContentBlock(text=element["text"])
                            _parts.append(_part)
                        elif element["type"] == "image_url":
                            format: Optional[str] = None
                            if isinstance(element["image_url"], dict):
                                image_url = element["image_url"]["url"]
                                format = element["image_url"].get("format")
                            else:
                                image_url = element["image_url"]
                            _part = BedrockImageProcessor.process_image_sync(  # type: ignore
                                image_url=image_url,
                                format=format,
                            )
                            _parts.append(_part)  # type: ignore
                        elif element["type"] == "file":
                            _part = (
                                BedrockConverseMessagesProcessor._process_file_message(
                                    message=cast(ChatCompletionFileObject, element)
                                )
                            )
                            _parts.append(_part)
                        elif element["type"] == "document":
                            _part = BedrockConverseMessagesProcessor._process_document_message(
                                element
                            )
                            _parts.append(_part)
                        _cache_point_block = (
                            litellm.AmazonConverseConfig()._get_cache_point_block(
                                message_block=cast(
                                    OpenAIMessageContentListBlock, element
                                ),
                                block_type="content_block",
                            )
                        )
                        if _cache_point_block is not None:
                            _parts.append(_cache_point_block)
                user_content.extend(_parts)
            elif message_block["content"] and isinstance(message_block["content"], str):
                _part = BedrockContentBlock(text=messages[msg_i]["content"])
                _cache_point_block = (
                    litellm.AmazonConverseConfig()._get_cache_point_block(
                        message_block, block_type="content_block"
                    )
                )
                user_content.append(_part)
                if _cache_point_block is not None:
                    user_content.append(_cache_point_block)

            msg_i += 1
        if user_content:
            if len(contents) > 0 and contents[-1]["role"] == "user":
                if (
                    assistant_continue_message is not None
                    or litellm.modify_params is True
                ):
                    # if last message was a 'user' message, then add a dummy assistant message (bedrock requires alternating roles)
                    contents = _insert_assistant_continue_message(
                        messages=contents,
                        assistant_continue_message=assistant_continue_message,
                    )
                    contents.append(
                        BedrockMessageBlock(role="user", content=user_content)
                    )
                else:
                    verbose_logger.warning(
                        "Potential consecutive user/tool blocks. Trying to merge. If error occurs, please set a 'assistant_continue_message' or set 'modify_params=True' to insert a dummy assistant message for bedrock calls."
                    )
                    contents[-1]["content"].extend(user_content)
            else:
                contents.append(BedrockMessageBlock(role="user", content=user_content))

        ## MERGE CONSECUTIVE TOOL CALL MESSAGES ##
        tool_content: List[BedrockContentBlock] = []
        while msg_i < len(messages) and messages[msg_i]["role"] == "tool":
            tool_call_result = _convert_to_bedrock_tool_call_result(messages[msg_i])
            current_message = messages[msg_i]

            # Add the tool result first
            tool_content.append(tool_call_result)

            # Check if we need to add a separate cachePoint block
            has_cache_control = False

            # Check for message-level cache_control
            if current_message.get("cache_control", None) is not None:
                has_cache_control = True
            # Check for content-level cache_control in list content
            elif isinstance(current_message.get("content"), list):
                for content_element in current_message["content"]:
                    if (
                        isinstance(content_element, dict)
                        and content_element.get("cache_control", None) is not None
                    ):
                        has_cache_control = True
                        break

            # Add a separate cachePoint block if cache_control is present
            if has_cache_control:
                cache_point_block = BedrockContentBlock(
                    cachePoint=CachePointBlock(type="default")
                )
                tool_content.append(cache_point_block)

            msg_i += 1
        # Deduplicate toolResult blocks with the same toolUseId
        tool_content = _deduplicate_bedrock_tool_content(tool_content)
        if tool_content:
            # if last message was a 'user' message, then add a blank assistant message (bedrock requires alternating roles)
            if len(contents) > 0 and contents[-1]["role"] == "user":
                if (
                    assistant_continue_message is not None
                    or litellm.modify_params is True
                ):
                    # if last message was a 'user' message, then add a dummy assistant message (bedrock requires alternating roles)
                    contents = _insert_assistant_continue_message(
                        messages=contents,
                        assistant_continue_message=assistant_continue_message,
                    )
                    contents.append(
                        BedrockMessageBlock(role="user", content=tool_content)
                    )
                else:
                    verbose_logger.warning(
                        "Potential consecutive user/tool blocks. Trying to merge. If error occurs, please set a 'assistant_continue_message' or set 'modify_params=True' to insert a dummy assistant message for bedrock calls."
                    )
                    contents[-1]["content"].extend(tool_content)
            else:
                contents.append(BedrockMessageBlock(role="user", content=tool_content))
        assistant_content: List[BedrockContentBlock] = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            assistant_message_block = get_assistant_message_block_or_continue_message(
                message=messages[msg_i],
                assistant_continue_message=assistant_continue_message,
            )
            _assistant_content = assistant_message_block.get("content", None)
            thinking_blocks = cast(
                Optional[List[ChatCompletionThinkingBlock]],
                assistant_message_block.get("thinking_blocks"),
            )

            if thinking_blocks is not None:
                converted_thinking_blocks = BedrockConverseMessagesProcessor.translate_thinking_blocks_to_reasoning_content_blocks(
                    thinking_blocks
                )
                assistant_content = BedrockConverseMessagesProcessor.add_thinking_blocks_to_assistant_content(
                    thinking_blocks=converted_thinking_blocks,
                    assistant_parts=assistant_content,
                )

            if _assistant_content is not None and isinstance(_assistant_content, list):
                assistants_parts: List[BedrockContentBlock] = []
                for element in _assistant_content:
                    if isinstance(element, dict):
                        if element["type"] == "thinking":
                            thinking_block = BedrockConverseMessagesProcessor.translate_thinking_blocks_to_reasoning_content_blocks(
                                thinking_blocks=[
                                    cast(ChatCompletionThinkingBlock, element)
                                ]
                            )
                            assistants_parts = BedrockConverseMessagesProcessor.add_thinking_blocks_to_assistant_content(
                                thinking_blocks=thinking_block,
                                assistant_parts=assistants_parts,
                            )
                        elif element["type"] == "text":
                            # AWS Bedrock doesn't allow empty or whitespace-only text content
                            # Skip completely empty strings to avoid blank content blocks
                            if element.get("text", "").strip():
                                assistants_part = BedrockContentBlock(
                                    text=element["text"]
                                )
                                assistants_parts.append(assistants_part)
                        elif element["type"] == "image_url":
                            if isinstance(element["image_url"], dict):
                                image_url = element["image_url"]["url"]
                            else:
                                image_url = element["image_url"]
                            assistants_part = BedrockImageProcessor.process_image_sync(  # type: ignore
                                image_url=image_url
                            )
                            assistants_parts.append(assistants_part)
                        # Add cache point block for assistant content elements
                        _cache_point_block = (
                            litellm.AmazonConverseConfig()._get_cache_point_block(
                                message_block=cast(
                                    OpenAIMessageContentListBlock, element
                                ),
                                block_type="content_block",
                            )
                        )
                        if _cache_point_block is not None:
                            assistants_parts.append(_cache_point_block)
                assistant_content.extend(assistants_parts)
            elif _assistant_content is not None and isinstance(_assistant_content, str):
                # Skip completely empty strings to avoid blank content blocks
                if _assistant_content.strip():
                    assistant_content.append(
                        BedrockContentBlock(text=_assistant_content)
                    )
                # Add cache point block for assistant string content
                _cache_point_block = (
                    litellm.AmazonConverseConfig()._get_cache_point_block(
                        assistant_message_block, block_type="content_block"
                    )
                )
                if _cache_point_block is not None:
                    assistant_content.append(_cache_point_block)
            _tool_calls = assistant_message_block.get("tool_calls", [])
            if _tool_calls:
                assistant_content.extend(
                    _convert_to_bedrock_tool_call_invoke(_tool_calls)
                )

            msg_i += 1

        assistant_content = _deduplicate_bedrock_content_blocks(
            assistant_content, "toolUse"
        )
        assistant_content = _sort_bedrock_assistant_content_blocks(assistant_content)

        if assistant_content:
            contents.append(
                BedrockMessageBlock(role="assistant", content=assistant_content)
            )

        if msg_i == init_msg_i:  # prevent infinite loops
            raise litellm.BadRequestError(
                message=BAD_MESSAGE_ERROR_STR + f"passed in {messages[msg_i]}",
                model=model,
                llm_provider=llm_provider,
            )

    return _rename_duplicate_bedrock_document_names(contents)

