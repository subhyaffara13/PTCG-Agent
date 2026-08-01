
def models_ls(
    repo_id: Annotated[
        str | None,
        typer.Argument(help="Model ID (e.g. `username/repo-name`) to list files from. If omitted, lists models."),
    ] = None,
    search: SearchOpt = None,
    author: AuthorOpt = None,
    filter: FilterOpt = None,
    num_parameters: Annotated[
        str | None,
        typer.Option(help="Filter by parameter count, e.g. 'min:6B,max:128B'."),
    ] = None,
    sort: Annotated[
        ModelSortEnum | None,
        typer.Option(help="Sort results."),
    ] = None,
    limit: LimitOpt = REPO_LIST_DEFAULT_LIMIT,
    expand: ExpandOpt = None,
    human_readable: Annotated[
        bool,
        typer.Option("--human-readable", "-h", help="Show sizes in human readable format (only for listing files)."),
    ] = False,
    as_tree: Annotated[
        bool,
        typer.Option("--tree", help="List files in tree format (only for listing files)."),
    ] = False,
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-R", help="List files recursively (only for listing files)."),
    ] = False,
    revision: RevisionOpt = None,
    token: TokenOpt = None,
) -> None:
    """List models on the Hub, or files in a model repo.

    When called with no argument, lists models on the Hub.
    When called with a model ID, lists files in that model repo.
    """
    if repo_id is not None:
        if search is not None:
            raise typer.BadParameter("Cannot use --search when listing files.")
        if author is not None:
            raise typer.BadParameter("Cannot use --author when listing files.")
        if filter is not None:
            raise typer.BadParameter("Cannot use --filter when listing files.")
        if num_parameters is not None:
            raise typer.BadParameter("Cannot use --num-parameters when listing files.")
        if sort is not None:
            raise typer.BadParameter("Cannot use --sort when listing files.")
        if limit != REPO_LIST_DEFAULT_LIMIT:
            raise typer.BadParameter("Cannot use --limit when listing files.")
        if expand is not None:
            raise typer.BadParameter("Cannot use --expand when listing files.")
        return list_repo_files_cmd(
            repo_id=repo_id,
            repo_type="model",
            human_readable=human_readable,
            as_tree=as_tree,
            recursive=recursive,
            revision=revision,
            token=token,
        )

    if as_tree:
        raise typer.BadParameter("Cannot use --tree when listing models.")
    if recursive:
        raise typer.BadParameter("Cannot use --recursive when listing models.")
    if human_readable:
        raise typer.BadParameter("Cannot use --human-readable when listing models.")
    if revision is not None:
        raise typer.BadParameter("Cannot use --revision when listing models.")
    api = get_hf_api(token=token)
    sort_key = sort.value if sort else None
    results = [
        _dataclass_to_dict(model_info)
        for model_info in api.list_models(
            filter=filter,
            author=author,
            search=search,
            num_parameters=num_parameters,
            sort=sort_key,
            limit=limit,
            expand=expand,  # type: ignore
        )
    ]
    out.table(results)

