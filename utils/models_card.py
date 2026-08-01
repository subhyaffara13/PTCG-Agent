
def models_card(
    model_id: Annotated[str, typer.Argument(help="The model ID (e.g. `username/repo-name`).")],
    metadata: Annotated[bool, typer.Option("--metadata", help="Output only the metadata from the card.")] = False,
    text: Annotated[bool, typer.Option("--text", help="Output only the text body (no metadata).")] = False,
    token: TokenOpt = None,
) -> None:
    """Get the model card (README) for a model on the Hub."""
    if metadata and text:
        raise CLIError("--metadata and --text are mutually exclusive.")
    card = ModelCard.load(model_id, token=token)
    if metadata:
        out.dict(card.data.to_dict())
    elif text:
        out.text(card.text)
    else:
        out.text(card.content)
        out.hint(f"Use `hf models card {model_id} --metadata` to extract only the card metadata.")

