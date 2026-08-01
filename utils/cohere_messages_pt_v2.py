
def cohere_messages_pt_v2(
    messages: List,
    model: str,
    llm_provider: str,
) -> Tuple[Union[str, ToolResultObject], ChatHistory]:
    """
    Returns a tuple(Union[tool_result, message], chat_history)

    - if last message is tool result -> return 'tool_result'
    - if last message is text -> return message (str)

    - return preceding messages as 'chat_history'

    Note:
    - cannot specify message if the last entry in chat history contains tool results
    - message must be at least 1 token long or tool results must be specified.
    - cannot specify tool_results if the last entry in chat history contains a user message
    """
    tool_calls: List = get_all_tool_calls(messages=messages)

    ## GET MOST RECENT MESSAGE
    most_recent_message = messages.pop(-1)
    returned_message: Union[ToolResultObject, str] = ""
    if (
        most_recent_message.get("role", "") is not None
        and most_recent_message["role"] == "tool"
    ):
        # tool result
        returned_message = convert_openai_message_to_cohere_tool_result(
            most_recent_message, tool_calls
        )
    else:
        content: Union[str, List] = most_recent_message.get("content")
        if isinstance(content, str):
            returned_message = content
        else:
            for chunk in content:
                if chunk.get("type") == "text":
                    returned_message += chunk.get("text")

    ## CREATE CHAT HISTORY
    user_message_types = {"user"}
    tool_message_types = {"tool", "function"}
    # reformat messages to ensure user/assistant are alternating, if there's either 2 consecutive 'user' messages or 2 consecutive 'assistant' message, merge them.
    new_messages: ChatHistory = []
    msg_i = 0

    while msg_i < len(messages):
        user_content: str = ""
        init_msg_i = msg_i
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] in user_message_types:
            if isinstance(messages[msg_i]["content"], list):
                for m in messages[msg_i]["content"]:
                    if m.get("type", "") == "text":
                        user_content += m["text"]
            else:
                user_content += messages[msg_i]["content"]
            msg_i += 1

        if len(user_content) > 0:
            new_messages.append(ChatHistoryUser(role="USER", message=user_content))

        system_content: str = ""
        ## MERGE CONSECUTIVE SYSTEM CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "system":
            if isinstance(messages[msg_i]["content"], list):
                for m in messages[msg_i]["content"]:
                    if m.get("type", "") == "text":
                        system_content += m["text"]
            else:
                system_content += messages[msg_i]["content"]
            msg_i += 1

        if len(system_content) > 0:
            new_messages.append(
                ChatHistorySystem(role="SYSTEM", message=system_content)
            )

        assistant_content: str = ""
        assistant_tool_calls: List[ToolCallObject] = []
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            if messages[msg_i].get("content", None) is not None and isinstance(
                messages[msg_i]["content"], list
            ):
                for m in messages[msg_i]["content"]:
                    if m.get("type", "") == "text":
                        assistant_content += m["text"]
            elif messages[msg_i].get("content") is not None and isinstance(
                messages[msg_i]["content"], str
            ):
                assistant_content += messages[msg_i]["content"]
            if messages[msg_i].get(
                "tool_calls", []
            ):  # support assistant tool invoke conversion
                assistant_tool_calls.extend(
                    convert_to_cohere_tool_invoke(messages[msg_i]["tool_calls"])
                )

            if messages[msg_i].get("function_call"):
                assistant_tool_calls.extend(
                    convert_to_cohere_tool_invoke(messages[msg_i]["function_call"])
                )

            msg_i += 1

        if len(assistant_content) > 0:
            new_messages.append(
                ChatHistoryChatBot(
                    role="CHATBOT",
                    message=assistant_content,
                    tool_calls=assistant_tool_calls,
                )
            )

        ## MERGE CONSECUTIVE TOOL RESULTS
        tool_results: List[ToolResultObject] = []
        while msg_i < len(messages) and messages[msg_i]["role"] in tool_message_types:
            tool_results.append(
                convert_openai_message_to_cohere_tool_result(
                    messages[msg_i], tool_calls
                )
            )

            msg_i += 1

        if len(tool_results) > 0:
            new_messages.append(
                ChatHistoryToolResult(role="TOOL", tool_results=tool_results)
            )

        if msg_i == init_msg_i:  # prevent infinite loops
            raise litellm.BadRequestError(
                message=BAD_MESSAGE_ERROR_STR + f"passed in {messages[msg_i]}",
                model=model,
                llm_provider=llm_provider,
            )

    return returned_message, new_messages

