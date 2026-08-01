
def move(
    from_id: Annotated[
        str,
        typer.Argument(
            help="Source bucket ID: namespace/bucket_name or hf://buckets/namespace/bucket_name",
        ),
    ],
    to_id: Annotated[
        str,
        typer.Argument(
            help="Destination bucket ID: namespace/bucket_name or hf://buckets/namespace/bucket_name",
        ),
    ],
    token: TokenOpt = None,
) -> None:
    """Move (rename) a bucket to a new name or namespace."""
    # Parse from_id
    parsed_from = _parse_bucket_uri(from_id)
    if parsed_from.path_in_repo:
        raise typer.BadParameter(
            f"Cannot specify a prefix for bucket move: {from_id}."
            f" Use namespace/bucket_name or {BUCKET_PREFIX}namespace/bucket_name."
        )

    # Parse to_id
    parsed_to = _parse_bucket_uri(to_id)
    if parsed_to.path_in_repo:
        raise typer.BadParameter(
            f"Cannot specify a prefix for bucket move: {to_id}."
            f" Use namespace/bucket_name or {BUCKET_PREFIX}namespace/bucket_name."
        )

    api = get_hf_api(token=token)
    api.move_bucket(from_id=parsed_from.id, to_id=parsed_to.id)
    out.result("Bucket moved", from_id=parsed_from.id, to_id=parsed_to.id)

