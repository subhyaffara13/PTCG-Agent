
def ollama_pt(
    model: str, messages: list
) -> Union[
    str, OllamaVisionModelObject
]:  # https://github.com/ollama/ollama/blob/af4cf55884ac54b9e637cd71dadfe9b7a5685877/docs/modelfile.md#template
    user_message_types = {"user", "tool", "function"}
    msg_i = 0
    images = []
    prompt = ""
    while msg_i < len(messages):
        init_msg_i = msg_i
        user_content_str = ""
        ## MERGE CONSECUTIVE USER CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] in user_message_types:
            msg_content = messages[msg_i].get("content")
            if msg_content:
                if isinstance(msg_content, list):
                    for m in msg_content:
                        if m.get("type", "") == "image_url":
                            if isinstance(m["image_url"], str):
                                images.append(m["image_url"])
                            elif isinstance(m["image_url"], dict):
                                images.append(m["image_url"]["url"])
                        elif m.get("type", "") == "text":
                            user_content_str += m["text"]
                else:
                    # Tool message content will always be a string
                    user_content_str += msg_content

            msg_i += 1

        if user_content_str:
            prompt += f"### User:\n{user_content_str}\n\n"

        system_content_str, msg_i = _handle_ollama_system_message(
            messages, prompt, msg_i
        )
        if system_content_str:
            prompt += f"### System:\n{system_content_str}\n\n"

        assistant_content_str = ""
        ## MERGE CONSECUTIVE ASSISTANT CONTENT ##
        while msg_i < len(messages) and messages[msg_i]["role"] == "assistant":
            assistant_content_str += convert_content_list_to_str(messages[msg_i])

            tool_calls = messages[msg_i].get("tool_calls")
            ollama_tool_calls = []
            if tool_calls:
                for call in tool_calls:
                    call_id: str = call["id"]
                    function_name: str = call["function"]["name"]
                    arguments = json.loads(call["function"]["arguments"])

                    ollama_tool_calls.append(
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": arguments,
                            },
                        }
                    )

            if ollama_tool_calls:
                assistant_content_str += (
                    f"Tool Calls: {json.dumps(ollama_tool_calls, indent=2)}"
                )

            msg_i += 1

        if assistant_content_str:
            prompt += f"### Assistant:\n{assistant_content_str}\n\n"

        if msg_i == init_msg_i:  # prevent infinite loops
            raise litellm.BadRequestError(
                message=BAD_MESSAGE_ERROR_STR + f"passed in {messages[msg_i]}",
                model=model,
                llm_provider="ollama",
            )

    response_dict: OllamaVisionModelObject = {
        "prompt": prompt,
        "images": images,
    }

    return response_dict

