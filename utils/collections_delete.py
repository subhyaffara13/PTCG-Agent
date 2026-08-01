
def collections_delete(
    collection_slug: Annotated[str, typer.Argument(help="The collection slug (e.g., 'username/collection-slug').")],
    missing_ok: Annotated[
        bool,
        typer.Option(help="Do not raise an error if the collection doesn't exist."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Delete a collection from the Hub."""
    api = get_hf_api(token=token)
    api.delete_collection(collection_slug, missing_ok=missing_ok)
    out.result("Collection deleted", slug=collection_slug)

