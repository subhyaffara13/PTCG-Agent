
def get_chatgpt_default_instructions() -> str:
    return os.getenv("CHATGPT_DEFAULT_INSTRUCTIONS") or CHATGPT_DEFAULT_INSTRUCTIONS

