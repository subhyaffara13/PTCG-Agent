
def mistral_instruct_pt(messages):
    # Following the Mistral example's https://huggingface.co/docs/transformers/main/chat_templating
    prompt = custom_prompt(
        initial_prompt_value="<s>",
        role_dict={
            "system": {
                "pre_message": "[INST] \n",
                "post_message": " [/INST]\n",
            },
            "user": {"pre_message": "[INST] ", "post_message": " [/INST]\n"},
            "assistant": {"pre_message": " ", "post_message": "</s> "},
        },
        final_prompt_value="",
        messages=messages,
    )
    return prompt

