
def datasets_card(
    dataset_id: Annotated[str, typer.Argument(help="The dataset ID (e.g. `username/repo-name`).")],
    metadata: Annotated[bool, typer.Option("--metadata", help="Output only the metadata from the card.")] = False,
    text: Annotated[bool, typer.Option("--text", help="Output only the text body (no metadata).")] = False,
    token: TokenOpt = None,
) -> None:
    """Get the dataset card (README) for a dataset on the Hub."""
    if metadata and text:
        raise CLIError("--metadata and --text are mutually exclusive.")
    card = DatasetCard.load(dataset_id, token=token)
    if metadata:
        out.dict(card.data.to_dict())
    elif text:
        out.text(card.text)
    else:
        out.text(card.content)
        out.hint(f"Use `hf datasets card {dataset_id} --metadata` to extract only the card metadata.")

