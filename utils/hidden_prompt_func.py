
def hidden_prompt_func(prompt: str) -> str:
    import getpass

    return getpass.getpass(prompt)

