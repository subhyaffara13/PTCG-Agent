
def prune(
    cache_dir: Annotated[
        str | None,
        typer.Option(
            help="Cache directory to scan (defaults to Hugging Face cache).",
        ),
    ] = None,
    yes: Annotated[
        bool,
        typer.Option(
            "-y",
            "--yes",
            help="Skip confirmation prompt.",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            help="Preview deletions without removing anything.",
        ),
    ] = False,
) -> None:
    """Remove detached revisions from the cache."""
    try:
        hf_cache_info = scan_cache_dir(cache_dir)
    except CacheNotFound as exc:
        raise CLIError(f"Cache directory not found: {exc.cache_dir}") from exc

    selected: dict[CachedRepoInfo, frozenset[CachedRevisionInfo]] = {}
    revisions: set[str] = set()
    for repo in hf_cache_info.repos:
        detached = frozenset(revision for revision in repo.revisions if len(revision.refs) == 0)
        if not detached:
            continue
        selected[repo] = detached
        revisions.update(revision.commit_hash for revision in detached)

    if len(revisions) == 0:
        out.text("No unreferenced revisions found. Nothing to prune.")
        return

    resolution = _DeletionResolution(
        revisions=frozenset(revisions),
        selected=selected,
        missing=(),
    )
    strategy = hf_cache_info.delete_revisions(*sorted(resolution.revisions))
    counts = summarize_deletions(selected)

    out.text(
        f"About to delete {counts.total_revision_count} unreferenced revision(s) ({strategy.expected_freed_size_str} total)."
    )
    print_cache_selected_revisions(selected)

    if dry_run:
        out.result(
            "Dry run: no files were deleted.",
            dry_run=True,
            revisions=counts.total_revision_count,
            size=strategy.expected_freed_size_str,
        )
        return

    out.confirm("Proceed?", yes=yes)

    strategy.execute()
    out.result(
        f"Deleted {counts.total_revision_count} unreferenced revision(s); freed {strategy.expected_freed_size_str}.",
        revisions_deleted=counts.total_revision_count,
        freed=strategy.expected_freed_size_str,
    )

