
def ls(
    cache_dir: Annotated[
        str | None,
        typer.Option(
            help="Cache directory to scan (defaults to Hugging Face cache).",
        ),
    ] = None,
    revisions: Annotated[
        bool,
        typer.Option(
            help="Include revisions in the output instead of aggregated repositories.",
        ),
    ] = False,
    filter: Annotated[
        list[str] | None,
        typer.Option(
            "-f",
            "--filter",
            help="Filter entries (e.g. 'size>1GB', 'type=model', 'accessed>7d'). Can be used multiple times.",
        ),
    ] = None,
    sort: Annotated[
        SortOptions | None,
        typer.Option(
            help="Sort entries by key. Supported keys: 'accessed', 'modified', 'name', 'size'. "
            "Append ':asc' or ':desc' to explicitly set the order (e.g., 'modified:asc'). "
            "Defaults: 'accessed', 'modified', 'size' default to 'desc' (newest/biggest first); "
            "'name' defaults to 'asc' (alphabetical).",
        ),
    ] = None,
    limit: Annotated[
        int | None,
        typer.Option(
            help="Limit the number of results returned. Returns only the top N entries after sorting.",
        ),
    ] = None,
) -> None:
    """List cached repositories or revisions."""
    try:
        hf_cache_info = scan_cache_dir(cache_dir)
    except CacheNotFound as exc:
        raise CLIError(f"Cache directory not found: {exc.cache_dir}") from exc

    filters = filter or []

    entries, repo_refs_map = collect_cache_entries(hf_cache_info, include_revisions=revisions)
    try:
        filter_fns = [compile_cache_filter(expr, repo_refs_map) for expr in filters]
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    now = time.time()
    for fn in filter_fns:
        entries = [entry for entry in entries if fn(entry[0], entry[1], now)]

    # Apply sorting if requested
    if sort:
        try:
            sort_key_fn, reverse = compile_cache_sort(sort.value)
            entries.sort(key=sort_key_fn, reverse=reverse)
        except ValueError as exc:
            raise typer.BadParameter(str(exc)) from exc

    # Apply limit if requested
    if limit is not None:
        if limit < 0:
            raise typer.BadParameter(f"Limit must be a positive integer, got {limit}.")
        entries = entries[:limit]

    if revisions:
        items = [
            {
                "id": repo.cache_id,
                "repo_id": repo.repo_id,
                "repo_type": repo.repo_type,
                "revision": revision.commit_hash,
                "snapshot_path": str(revision.snapshot_path),
                "size": revision.size_on_disk_str,
                "last_modified": revision.last_modified_str,
                "refs": sorted(revision.refs),
            }
            for repo, revision in entries
            if revision is not None
        ]
        out.table(
            items,
            headers=["id", "revision", "size", "last_modified", "refs"],
            id_key="revision",
            alignments={"size": "right"},
        )
    else:
        items = [
            {
                "id": repo.cache_id,
                "repo_id": repo.repo_id,
                "repo_type": repo.repo_type,
                "size": repo.size_on_disk_str,
                "last_accessed": repo.last_accessed_str or "",
                "last_modified": repo.last_modified_str,
                "refs": sorted(repo_refs_map.get(repo, frozenset())),
            }
            for repo, _ in entries
        ]
        out.table(
            items,
            headers=["id", "size", "last_accessed", "last_modified", "refs"],
            id_key="id",
            alignments={"size": "right"},
        )

    if entries:
        unique_repos = {repo for repo, _ in entries}
        repo_count = len(unique_repos)
        if revisions:
            revision_count = sum(1 for _, rev in entries if rev is not None)
            total_size = sum(rev.size_on_disk for _, rev in entries if rev is not None)
        else:
            revision_count = sum(len(repo.revisions) for repo in unique_repos)
            total_size = sum(repo.size_on_disk for repo in unique_repos)
        out.text(
            ANSI.bold(
                f"\nFound {repo_count} repo(s) for a total of {revision_count} revision(s)"
                f" and {_format_size(total_size)} on disk."
            )
        )


def ls(
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Lists all Inference Endpoints for the given namespace."""
    api = get_hf_api(token=token)
    try:
        endpoints = api.list_inference_endpoints(namespace=namespace, token=token)
    except HfHubHTTPError as error:
        out.error(f"Listing failed: {error}")
        raise typer.Exit(code=error.response.status_code) from error

    results = []
    for endpoint in endpoints:
        raw = endpoint.raw
        status = raw.get("status", {})
        model = raw.get("model", {})
        compute = raw.get("compute", {})
        provider = raw.get("provider", {})
        results.append(
            {
                "name": raw.get("name", ""),
                "model": model.get("repository", "") if isinstance(model, dict) else "",
                "status": status.get("state", "") if isinstance(status, dict) else "",
                "task": model.get("task", "") if isinstance(model, dict) else "",
                "framework": model.get("framework", "") if isinstance(model, dict) else "",
                "instance": compute.get("instanceType", "") if isinstance(compute, dict) else "",
                "vendor": provider.get("vendor", "") if isinstance(provider, dict) else "",
                "region": provider.get("region", "") if isinstance(provider, dict) else "",
            }
        )
    out.table(results, id_key="name")

