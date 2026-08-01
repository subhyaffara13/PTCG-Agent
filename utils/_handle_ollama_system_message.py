
def _handle_ollama_system_message(
    messages: list, prompt: str, msg_i: int
) -> Tuple[str, int]:
    system_content_str = ""
    ## MERGE CONSECUTIVE SYSTEM CONTENT ##
    while msg_i < len(messages) and messages[msg_i]["role"] == "system":
        msg_content = convert_content_list_to_str(messages[msg_i])
        system_content_str += msg_content

        msg_i += 1

    return system_content_str, msg_i

