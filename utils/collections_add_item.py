
def collections_add_item(
    collection_slug: Annotated[str, typer.Argument(help="The collection slug (e.g., 'username/collection-slug').")],
    item_id: Annotated[
        str, typer.Argument(help="The ID of the item to add (repo_id for repos, paper ID for papers).")
    ],
    item_type: Annotated[
        CollectionItemType,
        typer.Argument(help="The type of item (model, dataset, space, paper, collection, or bucket)."),
    ],
    note: Annotated[
        str | None,
        typer.Option(help="A note to attach to the item (max 500 characters)."),
    ] = None,
    exists_ok: Annotated[
        bool,
        typer.Option(help="Do not raise an error if the item is already in the collection."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Add an item to a collection."""
    api = get_hf_api(token=token)
    collection = api.add_collection_item(
        collection_slug=collection_slug,
        item_id=item_id,
        item_type=item_type.value,  # type: ignore[arg-type]
        note=note,
        exists_ok=exists_ok,
    )
    out.result("Item added to collection", slug=collection_slug, url=collection.url)

