
def discussion_create(
    repo_id: RepoIdArg,
    title: Annotated[
        str,
        typer.Option(
            "--title",
            help="The title of the discussion or pull request.",
        ),
    ],
    body: Annotated[
        str | None,
        typer.Option(
            "--body",
            help="The description (supports Markdown).",
        ),
    ] = None,
    body_file: Annotated[
        Path | None,
        typer.Option(
            "--body-file",
            help="Read the description from a file. Use '-' for stdin.",
        ),
    ] = None,
    pull_request: Annotated[
        bool,
        typer.Option(
            "--pull-request",
            "--pr",
            help="Create a pull request instead of a discussion.",
        ),
    ] = False,
    repo_type: RepoTypeOpt = RepoType.model,
    token: TokenOpt = None,
) -> None:
    """Create a new discussion or pull request on a repo."""
    description = _read_body(body, body_file)
    api = get_hf_api(token=token)
    discussion = api.create_discussion(
        repo_id=repo_id,
        title=title,
        description=description,
        repo_type=repo_type.value,
        pull_request=pull_request,
    )
    kind = "pull request" if pull_request else "discussion"
    ref = f"refs/pr/{discussion.num}" if pull_request else None
    out.result(f"Created {kind} #{discussion.num} on {repo_id}", num=discussion.num, url=discussion.url, ref=ref)

