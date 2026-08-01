
def anthropic_pt(
    messages: list,
):  # format - https://docs.anthropic.com/claude/reference/complete_post
    """
    You can "put words in Claude's mouth" by ending with an assistant message.
    See: https://docs.anthropic.com/claude/docs/put-words-in-claudes-mouth
    """

    class AnthropicConstants(Enum):
        HUMAN_PROMPT = "\n\nHuman: "
        AI_PROMPT = "\n\nAssistant: "

    prompt = ""
    for idx, message in enumerate(
        messages
    ):  # needs to start with `\n\nHuman: ` and end with `\n\nAssistant: `
        if message["role"] == "user":
            prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}{message['content']}"
        elif message["role"] == "system":
            prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}<admin>{message['content']}</admin>"
        else:
            prompt += f"{AnthropicConstants.AI_PROMPT.value}{message['content']}"
        if (
            idx == 0 and message["role"] == "assistant"
        ):  # ensure the prompt always starts with `\n\nHuman: `
            prompt = f"{AnthropicConstants.HUMAN_PROMPT.value}" + prompt
    if messages[-1]["role"] != "assistant":
        prompt += f"{AnthropicConstants.AI_PROMPT.value}"
    return prompt

