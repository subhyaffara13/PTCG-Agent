
def repo_list(
    namespace: Annotated[
        str | None,
        typer.Option(
            help="Organization name. If not provided, lists repos for the authenticated user.",
        ),
    ] = None,
    repo_type: Annotated[
        RepoTypeAll | None,
        typer.Option(
            "--type",
            "--repo-type",
            help="Filter by repository type (model, dataset, space, or bucket).",
        ),
    ] = None,
    search: SearchOpt = None,
    limit: LimitOpt = REPO_LIST_DEFAULT_LIMIT,
    explore: Annotated[
        bool,
        typer.Option("--explore", help="Explore your repos as an interactive 3D city."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """List all repos (models, datasets, spaces, buckets) with storage info."""
    api = get_hf_api(token=token)
    repos = list(api.list_user_repos(namespace=namespace))
    if repo_type is not None:
        repos = [r for r in repos if r.type == repo_type.value]
    if search is not None:
        search_lower = search.lower()
        repos = [r for r in repos if search_lower in r.id.lower()]
    total = len(repos)

    if explore:
        if out.mode == OutputFormat.human:
            run_city_game(repos)
            return
        raise CLIError("Repository exploration is only available in terminal.")

    if limit > 0:
        repos = repos[:limit]
    items = [
        {
            "id": r.id,
            "type": r.type,
            "updated": r.updated_at.strftime("%Y-%m-%d"),
            "visibility": r.visibility,
            "storage": format_size(r.storage, human_readable=True),
            "%_of_total": f"{r.storage_percent:.1f}%",
        }
        for r in repos
    ]
    out.table(items, id_key="id", alignments={"storage": "right", "%_of_total": "right"})
    if limit > 0 and total > limit:
        out.hint(f"Showing {limit} of {total} repos. Use `--limit 0` to list all.")

