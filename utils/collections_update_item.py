
def collections_update_item(
    collection_slug: Annotated[str, typer.Argument(help="The collection slug (e.g., 'username/collection-slug').")],
    item_object_id: Annotated[
        str,
        typer.Argument(help="The ID of the item in the collection (from 'item_object_id' field, not the repo_id)."),
    ],
    note: Annotated[
        str | None,
        typer.Option(help="A new note for the item (max 500 characters)."),
    ] = None,
    position: Annotated[
        int | None,
        typer.Option(help="The new position of the item in the collection."),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Update an item in a collection."""
    api = get_hf_api(token=token)
    api.update_collection_item(
        collection_slug=collection_slug,
        item_object_id=item_object_id,
        note=note,
        position=position,
    )
    out.result("Item updated in collection", slug=collection_slug)

