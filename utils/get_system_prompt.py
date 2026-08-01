
def get_system_prompt(messages):
    system_prompt_indices = []
    system_prompt = ""
    for idx, message in enumerate(messages):
        if message["role"] == "system":
            system_prompt += message["content"]
            system_prompt_indices.append(idx)
    if len(system_prompt_indices) > 0:
        for idx in reversed(system_prompt_indices):
            messages.pop(idx)
    return system_prompt, messages

