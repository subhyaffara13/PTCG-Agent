
def collections_ls(
    owner: Annotated[
        str | None,
        typer.Option(help="Filter by owner username or organization."),
    ] = None,
    item: Annotated[
        str | None,
        typer.Option(
            help='Filter collections containing a specific item (e.g., "models/gpt2", "datasets/squad", "papers/2311.12983").'
        ),
    ] = None,
    sort: Annotated[
        CollectionSort | None,
        typer.Option(help="Sort results by last modified, trending, or upvotes."),
    ] = None,
    limit: LimitOpt = 10,
    token: TokenOpt = None,
) -> None:
    """List collections on the Hub."""
    api = get_hf_api(token=token)
    sort_key = sort.value if sort else None
    results = [
        _dataclass_to_dict(collection)
        for collection in api.list_collections(
            owner=owner,
            item=item,
            sort=sort_key,  # type: ignore[arg-type]
            limit=limit,
        )
    ]
    out.table(results)

