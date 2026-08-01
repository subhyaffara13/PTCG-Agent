
def papers_search(
    query: Annotated[str, typer.Argument(help="Search query string.")],
    limit: LimitOpt = 20,
    token: TokenOpt = None,
) -> None:
    """Search papers on the Hub."""
    api = get_hf_api(token=token)
    results = [_dataclass_to_dict(paper_info) for paper_info in api.list_papers(query=query, limit=limit)]
    out.table(results, headers=["id", "title", "summary", "upvotes", "published_at"])

