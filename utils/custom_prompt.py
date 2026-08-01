
def custom_prompt(
    role_dict: dict,
    messages: list,
    initial_prompt_value: str = "",
    final_prompt_value: str = "",
    bos_token: str = "",
    eos_token: str = "",
) -> str:
    prompt = bos_token + initial_prompt_value
    bos_open = True
    ## a bos token is at the start of a system / human message
    ## an eos token is at the end of the assistant response to the message
    for message in messages:
        role = message["role"]

        if role in ["system", "human"] and not bos_open:
            prompt += bos_token
            bos_open = True

        pre_message_str = (
            role_dict[role]["pre_message"]
            if role in role_dict and "pre_message" in role_dict[role]
            else ""
        )
        post_message_str = (
            role_dict[role]["post_message"]
            if role in role_dict and "post_message" in role_dict[role]
            else ""
        )
        if isinstance(message["content"], str):
            prompt += pre_message_str + message["content"] + post_message_str
        elif isinstance(message["content"], list):
            text_str = ""
            for content in message["content"]:
                if content.get("text", None) is not None and isinstance(
                    content["text"], str
                ):
                    text_str += content["text"]
            prompt += pre_message_str + text_str + post_message_str

        if role == "assistant":
            prompt += eos_token
            bos_open = False

    prompt += final_prompt_value
    return prompt

