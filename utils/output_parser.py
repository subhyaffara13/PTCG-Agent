
def output_parser(generated_text: str):
    """
    Parse the output text to remove any special characters. In our current approach we just check for ChatML tokens.

    Initial issue that prompted this - https://github.com/BerriAI/litellm/issues/763
    """
    chat_template_tokens = ["<|assistant|>", "<|system|>", "<|user|>", "<s>", "</s>"]
    for token in chat_template_tokens:
        if generated_text.strip().startswith(token):
            generated_text = generated_text.replace(token, "", 1)
        if generated_text.endswith(token):
            generated_text = generated_text[::-1].replace(token[::-1], "", 1)[::-1]
    return generated_text

