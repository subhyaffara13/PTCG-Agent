
def rm(
    targets: Annotated[
        list[str],
        typer.Argument(
            help="One or more repo IDs (e.g. model/bert-base-uncased), repo-level hf:// URIs, or revision hashes to delete.",
        ),
    ],
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
    """Remove cached repositories or revisions."""
    try:
        hf_cache_info = scan_cache_dir(cache_dir)
    except CacheNotFound as exc:
        raise CLIError(f"Cache directory not found: {exc.cache_dir}") from exc

    resolution = _resolve_deletion_targets(hf_cache_info, targets)

    if resolution.missing:
        details = "\n".join(f"  - {entry}" for entry in resolution.missing)
        out.warning(f"Could not find in cache:\n{details}")

    if len(resolution.revisions) == 0:
        out.text("Nothing to delete.")
        raise typer.Exit(code=0)

    strategy = hf_cache_info.delete_revisions(*sorted(resolution.revisions))
    counts = summarize_deletions(resolution.selected)

    summary_parts: list[str] = []
    if counts.repo_count:
        summary_parts.append(f"{counts.repo_count} repo(s)")
    if counts.partial_revision_count:
        summary_parts.append(f"{counts.partial_revision_count} revision(s)")
    if not summary_parts:
        summary_parts.append(f"{counts.total_revision_count} revision(s)")

    summary_text = " and ".join(summary_parts)
    out.text(f"About to delete {summary_text} totalling {strategy.expected_freed_size_str}.")
    print_cache_selected_revisions(resolution.selected)

    if dry_run:
        out.result(
            "Dry run: no files were deleted.",
            dry_run=True,
            repos=counts.repo_count,
            revisions=counts.total_revision_count,
            size=strategy.expected_freed_size_str,
        )
        return

    out.confirm("Proceed with deletion?", yes=yes)

    strategy.execute()
    counts = summarize_deletions(resolution.selected)
    out.result(
        f"Deleted {counts.repo_count} repo(s) and {counts.total_revision_count} revision(s);"
        f" freed {strategy.expected_freed_size_str}.",
        repos_deleted=counts.repo_count,
        revisions_deleted=counts.total_revision_count,
        freed=strategy.expected_freed_size_str,
    )

