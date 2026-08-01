
def collections_delete_item(
    collection_slug: Annotated[str, typer.Argument(help="The collection slug (e.g., 'username/collection-slug').")],
    item_object_id: Annotated[
        str,
        typer.Argument(
            help="The ID of the item in the collection (retrieved from `item_object_id` field returned by 'hf collections info'."
        ),
    ],
    missing_ok: Annotated[
        bool,
        typer.Option(help="Do not raise an error if the item doesn't exist."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Delete an item from a collection."""
    api = get_hf_api(token=token)
    api.delete_collection_item(
        collection_slug=collection_slug,
        item_object_id=item_object_id,
        missing_ok=missing_ok,
    )
    out.result("Item deleted from collection", slug=collection_slug)

