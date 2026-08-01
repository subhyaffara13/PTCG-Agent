
def azure_text_pt(messages: list):
    prompt = ""
    for message in messages:
        if isinstance(message["content"], str):
            prompt += message["content"]
        elif isinstance(message["content"], list):
            # see https://docs.litellm.ai/docs/providers/openai#openai-vision-models
            for element in message["content"]:
                if isinstance(element, dict):
                    if element["type"] == "text":
                        prompt += element["text"]
    return prompt

