
def llama_2_chat_pt(messages):
    prompt = custom_prompt(
        role_dict={
            "system": {
                "pre_message": "[INST] <<SYS>>\n",
                "post_message": "\n<</SYS>>\n [/INST]\n",
            },
            "user": {  # follow this format https://github.com/facebookresearch/llama/blob/77062717054710e352a99add63d160274ce670c6/llama/generation.py#L348
                "pre_message": "[INST] ",
                "post_message": " [/INST]\n",
            },
            "assistant": {
                "post_message": "\n"  # follows this - https://replicate.com/blog/how-to-prompt-llama
            },
        },
        messages=messages,
        bos_token="<s>",
        eos_token="</s>",
    )
    return prompt

