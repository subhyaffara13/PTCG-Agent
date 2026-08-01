
def list_repo_files_cmd(
    repo_id: str,
    repo_type: str,
    human_readable: bool,
    as_tree: bool,
    recursive: bool,
    revision: str | None,
    token: str | None,
) -> None:
    """List files in a repo on the Hub. Used by models/datasets/spaces ls commands."""
    if as_tree and out.mode == OutputFormat.json:
        raise typer.BadParameter("Cannot use --tree with --format json.")

    api = get_hf_api(token=token)
    items = list(api.list_repo_tree(repo_id, recursive=recursive, revision=revision, repo_type=repo_type, expand=True))
    print_file_listing(items, human_readable=human_readable, as_tree=as_tree, recursive=recursive)

