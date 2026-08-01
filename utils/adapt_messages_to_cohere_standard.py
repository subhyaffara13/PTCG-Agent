
def adapt_messages_to_cohere_standard(
    messages: List[AllMessageValues],
) -> List[CohereMessage]:
    """Build a Cohere ``chatHistory`` list from an OpenAI-format message array.

    - All messages except the *last user message* are included. The caller pulls
      the last user message into the request's top-level ``message`` field, so
      trailing tool results (the standard agentic continuation pattern) still
      appear in ``chatHistory`` and reach the model.
    - If no user message exists, every message is included (no slice).
    - System messages must be filtered out by the caller (they are routed into
      ``preambleOverride`` separately) — they are not represented in
      ``chatHistory``.
    - Tool results are expressed as OCI ``CohereToolMessage.toolResults`` entries,
      with the originating call's name and parameters resolved from the preceding
      assistant message via a ``tool_call_id`` lookup.
    """
    # First pass: build tool_call_id → CohereToolCall so tool-result messages can
    # reference the originating call by name and parameters.
    tool_call_lookup: Dict[str, CohereToolCall] = {}
    for msg in messages:
        if msg.get("role") == "assistant":
            tool_calls_raw: Any = msg.get("tool_calls") or []
            for tc in tool_calls_raw:
                tc_id = tc.get("id", "")
                raw_args: Any = tc.get("function", {}).get("arguments", "{}")
                try:
                    params: Dict[str, Any] = (
                        json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                    )
                except json.JSONDecodeError:
                    params = {}
                tool_call_lookup[tc_id] = CohereToolCall(
                    name=str(tc.get("function", {}).get("name", "")),
                    parameters=params,
                )

    last_user_index = next(
        (
            i
            for i in range(len(messages) - 1, -1, -1)
            if messages[i].get("role") == "user"
        ),
        None,
    )
    history_source = (
        messages
        if last_user_index is None
        else [m for i, m in enumerate(messages) if i != last_user_index]
    )

    chat_history: List[CohereMessage] = []
    for msg in history_source:
        role = msg.get("role")
        content = _extract_text_content(msg.get("content"))

        tool_calls: Optional[List[CohereToolCall]] = None
        if role == "assistant" and msg.get("tool_calls"):  # type: ignore[union-attr,typeddict-item]
            tool_calls = []
            for tc in msg["tool_calls"]:  # type: ignore[union-attr,typeddict-item]
                raw_arguments: Any = tc.get("function", {}).get("arguments", {})
                if isinstance(raw_arguments, str):
                    try:
                        arguments: Dict[str, Any] = json.loads(raw_arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                else:
                    arguments = raw_arguments
                tool_calls.append(
                    CohereToolCall(
                        name=str(tc.get("function", {}).get("name", "")),
                        parameters=arguments,
                    )
                )

        if role == "user":
            chat_history.append(CohereMessage(role="USER", message=content))
        elif role == "assistant":
            chat_history.append(
                CohereMessage(role="CHATBOT", message=content, toolCalls=tool_calls)
            )
        elif role == "tool":
            tool_call_id = str(msg.get("tool_call_id", "") or "")
            cohere_call = tool_call_lookup.get(
                tool_call_id, CohereToolCall(name="", parameters={})
            )
            tool_result = CohereToolResult(
                call=cohere_call,
                outputs=[{"output": content}],
            )
            # OpenAI emits one tool-role message per parallel tool call, but
            # the OCI Cohere API expects all results from a single assistant
            # turn to share one TOOL history entry with multiple toolResults.
            # Merge consecutive tool messages so the model sees the parallel
            # call/result pairing correctly during agentic loops.
            if chat_history and isinstance(chat_history[-1], CohereToolMessage):
                chat_history[-1].toolResults.append(tool_result)
            else:
                chat_history.append(CohereToolMessage(toolResults=[tool_result]))

    return chat_history

