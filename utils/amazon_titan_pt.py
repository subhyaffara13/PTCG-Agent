
def amazon_titan_pt(
    messages: list,
):  # format - https://github.com/BerriAI/litellm/issues/1896
    """
    Amazon Titan uses 'User:' and 'Bot: in it's prompt template
    """

    class AmazonTitanConstants(Enum):
        HUMAN_PROMPT = "\n\nUser: "  # Assuming this is similar to Anthropic prompt formatting, since amazon titan's prompt formatting is currently undocumented
        AI_PROMPT = "\n\nBot: "

    prompt = ""
    for idx, message in enumerate(messages):
        if message["role"] == "user":
            prompt += f"{AmazonTitanConstants.HUMAN_PROMPT.value}{message['content']}"
        elif message["role"] == "system":
            prompt += f"{AmazonTitanConstants.HUMAN_PROMPT.value}<admin>{message['content']}</admin>"
        else:
            prompt += f"{AmazonTitanConstants.AI_PROMPT.value}{message['content']}"
        if (
            idx == 0 and message["role"] == "assistant"
        ):  # ensure the prompt always starts with `\n\nHuman: `
            prompt = f"{AmazonTitanConstants.HUMAN_PROMPT.value}" + prompt
    if messages[-1]["role"] != "assistant":
        prompt += f"{AmazonTitanConstants.AI_PROMPT.value}"
    return prompt

