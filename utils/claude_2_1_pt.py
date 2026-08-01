
def claude_2_1_pt(
    messages: list,
):  # format - https://docs.anthropic.com/claude/docs/how-to-use-system-prompts
    """
    Claude v2.1 allows system prompts (no Human: needed), but requires it be followed by Human:
    - you can't just pass a system message
    - you can't pass a system message and follow that with an assistant message
    if system message is passed in, you can only do system, human, assistant or system, human

    if a system message is passed in and followed by an assistant message, insert a blank human message between them.

    Additionally, you can "put words in Claude's mouth" by ending with an assistant message.
    See: https://docs.anthropic.com/claude/docs/put-words-in-claudes-mouth
    """

    class AnthropicConstants(Enum):
        HUMAN_PROMPT = "\n\nHuman: "
        AI_PROMPT = "\n\nAssistant: "

    prompt = ""
    for idx, message in enumerate(messages):
        if message["role"] == "user":
            prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}{message['content']}"
        elif message["role"] == "system":
            prompt += f"{message['content']}"
        elif message["role"] == "assistant":
            if idx > 0 and messages[idx - 1]["role"] == "system":
                prompt += f"{AnthropicConstants.HUMAN_PROMPT.value}"  # Insert a blank human message
            prompt += f"{AnthropicConstants.AI_PROMPT.value}{message['content']}"
    if messages[-1]["role"] != "assistant":
        prompt += f"{AnthropicConstants.AI_PROMPT.value}"  # prompt must end with \"\n\nAssistant: " turn
    return prompt

