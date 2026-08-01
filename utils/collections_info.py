
def collections_info(
    collection_slug: Annotated[str, typer.Argument(help="The collection slug (e.g., 'username/collection-slug').")],
    token: TokenOpt = None,
) -> None:
    """Get info about a collection on the Hub."""
    api = get_hf_api(token=token)
    collection = api.get_collection(collection_slug)
    out.dict(collection)

