
def collections_update(
    collection_slug: Annotated[str, typer.Argument(help="The collection slug (e.g., 'username/collection-slug').")],
    title: Annotated[
        str | None,
        typer.Option(help="The new title for the collection."),
    ] = None,
    description: Annotated[
        str | None,
        typer.Option(help="The new description for the collection."),
    ] = None,
    position: Annotated[
        int | None,
        typer.Option(help="The new position of the collection in the owner's list."),
    ] = None,
    private: Annotated[
        bool | None,
        typer.Option(help="Whether the collection should be private."),
    ] = None,
    theme: Annotated[
        str | None,
        typer.Option(help="The theme color for the collection (e.g., 'green', 'blue')."),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Update a collection's metadata on the Hub."""
    api = get_hf_api(token=token)
    collection = api.update_collection_metadata(
        collection_slug=collection_slug,
        title=title,
        description=description,
        position=position,
        private=private,
        theme=theme,
    )
    out.result("Collection updated", slug=collection.slug, url=collection.url)

