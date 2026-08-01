
def _parse_watch(values: list[str]) -> list[WebhookWatchedItem]:
    """Parse 'type:name' strings into WebhookWatchedItem objects.

    Args:
        values: List of strings in the format 'type:name'
            (e.g., 'model:bert-base-uncased', 'org:HuggingFace').

    Returns:
        List of WebhookWatchedItem objects.

    Raises:
        typer.BadParameter: If any value doesn't match the expected format.
    """
    items = []
    valid_types = tuple(_WATCHED_TYPES)
    for v in values:
        if ":" not in v:
            raise typer.BadParameter(
                f"Expected format 'type:name' (e.g. 'model:bert-base-uncased'), got '{v}'."
                f" Valid types: {', '.join(valid_types)}."
            )
        kind, name = v.split(":", 1)
        if kind not in valid_types:
            raise typer.BadParameter(f"Invalid type '{kind}'. Valid types: {', '.join(valid_types)}.")
        items.append(WebhookWatchedItem(type=kind, name=name))  # type: ignore
    return items

