
def spaces_search(
    query: Annotated[str, typer.Argument(help="Search query.")],
    filter: FilterOpt = None,
    sdk: Annotated[list[str] | None, typer.Option(help="Filter by SDK (e.g. gradio, docker, static).")] = None,
    include_non_running: Annotated[bool, typer.Option(help="Include non-running spaces in results.")] = False,
    description: Annotated[bool, typer.Option(help="Show AI-generated descriptions.")] = False,
    limit: LimitOpt = 10,
    token: TokenOpt = None,
) -> None:
    """Search spaces on the Hub using semantic search."""
    api = get_hf_api(token=token)
    results = api.search_spaces(
        query=query,
        filter=filter,
        sdk=sdk,
        include_non_running=include_non_running,
        token=token,
    )
    items = []
    for r in itertools.islice(results, limit):
        item: dict = {
            "id": r.id,
            "title": r.title,
            "sdk": r.sdk,
            "likes": r.likes,
            "stage": r.runtime.stage if r.runtime else None,
            "category": r.ai_category,
            "score": round(r.semantic_relevancy_score, 2) if r.semantic_relevancy_score is not None else None,
        }
        if description:
            item["description"] = r.ai_short_description
        items.append(item)
    out.table(items)
    if not description:
        out.hint("Use --description to show AI-generated descriptions.")

