
def collections_create(
    title: Annotated[str, typer.Argument(help="The title of the collection.")],
    namespace: Annotated[
        str | None,
        typer.Option(help="The namespace (username or organization). Defaults to the authenticated user."),
    ] = None,
    description: Annotated[
        str | None,
        typer.Option(help="A description for the collection."),
    ] = None,
    private: Annotated[
        bool,
        typer.Option(help="Create a private collection."),
    ] = False,
    exists_ok: Annotated[
        bool,
        typer.Option(help="Do not raise an error if the collection already exists."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Create a new collection on the Hub."""
    api = get_hf_api(token=token)
    collection = api.create_collection(
        title=title,
        namespace=namespace,
        description=description,
        private=private,
        exists_ok=exists_ok,
    )
    out.result("Collection created", slug=collection.slug, url=collection.url)

