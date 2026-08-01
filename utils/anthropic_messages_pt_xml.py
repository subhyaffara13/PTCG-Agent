
def anthropic_messages_pt_xml(messages: list):
    """
    format messages for anthropic
    1. Anthropic supports roles like "user" and "assistant", (here litellm translates system-> assistant)
    2. The first message always needs to be of role "user"
    3. Each message must alternate between "user" and "assistant" (this is not addressed as now by litellm)
    4. final assistant content cannot end with trailing whitespace (anthropic raises an error otherwise)
    5. System messages are a separate param to the Messages API (used for tool calling)
    6. Ensure we only accept role, content. (message.name is not supported)
    """
    # add role=tool support to allow function call result/error submission
    user_message_types = {"user", "tool"}
    # reformat messages to ensure user/assistant are alternating, if there's either 2 consecutive 'user' messages or 2 consecutive 'assistant' message, merge them.
    new_messages = []
    msg_i = 0
    while msg_i < len(messages):
        user_content = []
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] in user_message_types:
            if isinstance(messages[msg_i]["content"], list):
                for m in messages[msg_i]["content"]:
                    if m.get("type", "") == "image_url":
                        format = (
                            m["image_url"].get("format")
                            if isinstance(m["image_url"], dict)
                            else None
                        )
                        image_param = create_anthropic_image_param(
                            m["image_url"], format=format
                        )
                        # Convert to dict format for XML version
                        source = image_param["source"]
                        if isinstance(source, dict) and source.get("type") == "url":
                            # Type narrowing for URL source
                            url_source = cast(AnthropicContentParamSourceUrl, source)
                            user_content.append(
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "url",
                                        "url": url_source["url"],
                                    },
                                }
                            )
                        else:
                            # Type narrowing for base64 source
                            base64_source = cast(AnthropicContentParamSource, source)
                            user_content.append(
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": base64_source["media_type"],
                                        "data": base64_source["data"],
                                    },
                                }
                            )
                    elif m.get("type", "") == "text":
                        user_content.append({"type": "text", "text": m["text"]})
            else:
                # Tool message content will always be a string
                user_content.append(
                    {
                        "type": "text",
                        "text": (
                            convert_to_anthropic_tool_result_xml(messages[msg_i])
                            if messages[msg_i]["role"] == "tool"
                            else messages[msg_i]["content"]
                        ),
                    }
                )

            msg_i += 1

        if user_content:
            new_messages.append({"role": "user", "content": user_content})

        assistant_content = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            assistant_text = (
                messages[msg_i].get("content") or ""
            )  # either string or none
            if messages[msg_i].get(
                "tool_calls", []
            ):  # support assistant tool invoke conversion
                assistant_text += convert_to_anthropic_tool_invoke_xml(  # type: ignore
                    messages[msg_i]["tool_calls"]
                )

            assistant_content.append({"type": "text", "text": assistant_text})
            msg_i += 1

        if assistant_content:
            new_messages.append({"role": "assistant", "content": assistant_content})

    if not new_messages or new_messages[0]["role"] != "user":
        if litellm.modify_params:
            new_messages.insert(
                0, {"role": "user", "content": [{"type": "text", "text": "."}]}
            )
        else:
            raise Exception(
                "Invalid first message. Should always start with 'role'='user' for Anthropic. System prompt is sent separately for Anthropic. set 'litellm.modify_params = True' or 'litellm_settings:modify_params = True' on proxy, to insert a placeholder user message - '.' as the first message, "
            )

    if new_messages[-1]["role"] == "assistant":
        for content in new_messages[-1]["content"]:
            if isinstance(content, dict) and content["type"] == "text":
                content["text"] = content[
                    "text"
                ].rstrip()  # no trailing whitespace for final assistant message

    return new_messages

