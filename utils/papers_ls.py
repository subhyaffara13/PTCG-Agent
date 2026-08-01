
def papers_ls(
    date: Annotated[
        str | None,
        typer.Option(
            help="Date in ISO format (YYYY-MM-DD) or 'today'.",
            callback=_parse_date,
        ),
    ] = None,
    week: Annotated[
        str | None,
        typer.Option(help="ISO week to filter by, e.g. '2025-W09'."),
    ] = None,
    month: Annotated[
        str | None,
        typer.Option(help="Month to filter by in ISO format (YYYY-MM), e.g. '2025-02'."),
    ] = None,
    submitter: Annotated[
        str | None,
        typer.Option(help="Filter by username of the submitter."),
    ] = None,
    sort: Annotated[
        PaperSortEnum | None,
        typer.Option(help="Sort results."),
    ] = None,
    limit: LimitOpt = 50,
    token: TokenOpt = None,
) -> None:
    """List daily papers on the Hub."""
    api = get_hf_api(token=token)
    sort_key = sort.value if sort else None
    results = []
    for paper_info in api.list_daily_papers(
        date=date,
        week=week,
        month=month,
        submitter=submitter,
        sort=sort_key,
        limit=limit,
    ):
        item = _dataclass_to_dict(paper_info)
        submitted_by = item.get("submitted_by") or {}
        item["submitted_by_name"] = submitted_by.get("fullname") or submitted_by.get("username") or ""
        results.append(item)
    out.table(
        results,
        headers=["id", "title", "upvotes", "comments", "published_at", "submitted_by_name"],
    )

