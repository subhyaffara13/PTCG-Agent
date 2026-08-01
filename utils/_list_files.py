
def _list_files(
    argument: str,
    human_readable: bool,
    as_tree: bool,
    recursive: bool,
    token: str | None,
) -> None:
    """List files in a bucket."""
    if as_tree and out.mode == OutputFormat.json:
        raise typer.BadParameter("Cannot use --tree with --format json.")

    api = get_hf_api(token=token)
    parsed = _parse_bucket_uri(argument)
    items = list(
        api.list_bucket_tree(
            parsed.id,
            prefix=parsed.path_in_repo or None,
            recursive=recursive,
        )
    )

    print_file_listing(items, human_readable=human_readable, as_tree=as_tree, recursive=recursive)

