
def create_pretrained_tokenizer(
    identifier: str, revision="main", auth_token: Optional[str] = None
):
    """
    Creates a tokenizer from an existing file on a HuggingFace repository to be used with `token_counter`.

    Args:
    identifier (str): The identifier of a Model on the Hugging Face Hub, that contains a tokenizer.json file
    revision (str, defaults to main): A branch or commit id
    auth_token (str, optional, defaults to None): An optional auth token used to access private repositories on the Hugging Face Hub

    Returns:
    dict: A dictionary with the tokenizer and its type.
    """

    try:
        tokenizer = Tokenizer.from_pretrained(
            identifier, revision=revision, auth_token=auth_token  # type: ignore
        )
    except Exception as e:
        verbose_logger.error(
            f"Error creating pretrained tokenizer: {e}. Defaulting to version without 'auth_token'."
        )
        tokenizer = Tokenizer.from_pretrained(identifier, revision=revision)
    return {"type": "huggingface_tokenizer", "tokenizer": tokenizer}

