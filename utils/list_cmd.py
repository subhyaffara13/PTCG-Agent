
def list_cmd(
    argument: Annotated[
        str | None,
        typer.Argument(
            help=(
                "Namespace (user or org) to list buckets, or bucket ID"
                " (namespace/bucket_name(/prefix) or hf://buckets/...) to list files."
            ),
        ),
    ] = None,
    human_readable: Annotated[
        bool,
        typer.Option(
            "--human-readable",
            "-h",
            help="Show sizes in human readable format.",
        ),
    ] = False,
    as_tree: Annotated[
        bool,
        typer.Option(
            "--tree",
            help="List files in tree format (only for listing files).",
        ),
    ] = False,
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-R",
            help="List files recursively (only for listing files).",
        ),
    ] = False,
    search: SearchOpt = None,
    token: TokenOpt = None,
) -> None:
    """List buckets or files in a bucket.

    When called with no argument or a namespace, lists buckets.
    When called with a bucket ID (namespace/bucket_name), lists files in the bucket.
    """
    # Determine mode: listing buckets or listing files
    is_file_mode = argument is not None and _is_bucket_id(argument)

    if is_file_mode:
        if search is not None:
            raise typer.BadParameter("Cannot use --search when listing files.")
        _list_files(
            argument=argument,  # type: ignore
            human_readable=human_readable,
            as_tree=as_tree,
            recursive=recursive,
            token=token,
        )
    else:
        _list_buckets(
            namespace=argument,
            search=search,
            human_readable=human_readable,
            as_tree=as_tree,
            recursive=recursive,
            token=token,
        )

