
def create_and_tag_model_card(repo_id: str, tags: list[str] | None = None, token: str | None = None) -> ModelCard:
    """
    Creates or loads an existing model card and tags it.

    Args:
        repo_id (`str`):
            The repo_id where to look for the model card.
        tags (`list[str]`, *optional*):
            The list of tags to add in the model card
        token (`str`, *optional*):
            Authentication token, obtained with `huggingface_hub.HfApi.login` method. Will default to the stored token.
    """
    try:
        # Check if the model card is present on the remote repo
        model_card = ModelCard.load(repo_id, token=token)
    except EntryNotFoundError:
        # Otherwise create a simple model card from template
        model_description = "This is the model card of a 🤗 transformers model that has been pushed on the Hub. This model card has been automatically generated."
        card_data = ModelCardData(tags=[] if tags is None else tags, library_name="transformers")
        model_card = ModelCard.from_template(card_data, model_description=model_description)

    if tags is not None:
        # Ensure model_card.data.tags is a list and not None
        if model_card.data.tags is None:
            model_card.data.tags = []
        for model_tag in tags:
            if model_tag not in model_card.data.tags:
                model_card.data.tags.append(model_tag)

    return model_card

