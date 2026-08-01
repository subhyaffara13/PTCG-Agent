
def deepseek_r1_pt(messages):
    return hf_chat_template(
        model="deepseek-r1/deepseek-r1-7b-instruct", messages=messages
    )

