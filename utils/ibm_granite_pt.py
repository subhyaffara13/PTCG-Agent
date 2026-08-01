
def ibm_granite_pt(messages: list):
    """
    IBM's Granite models uses the template:
    <|system|> {system_message} <|user|> {user_message} <|assistant|> {assistant_message}

    See: https://www.ibm.com/docs/en/watsonx-as-a-service?topic=solutions-supported-foundation-models
    """
    return custom_prompt(
        messages=messages,
        role_dict={
            "system": {
                "pre_message": "<|system|>\n",
                "post_message": "\n",
            },
            "user": {
                "pre_message": "<|user|>\n",
                # Assistant tag is needed in the prompt after the user message
                # to avoid the model completing the users sentence before it answers
                # https://www.ibm.com/docs/en/watsonx/w-and-w/2.0.x?topic=models-granite-13b-chat-v2-prompting-tips#chat
                "post_message": "\n<|assistant|>\n",
            },
            "assistant": {
                "pre_message": "",
                "post_message": "\n",
            },
        },
    ).strip()

