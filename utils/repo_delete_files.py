
def repo_delete_files(
    repo_id: RepoIdArg,
    patterns: Annotated[
        list[str],
        typer.Argument(
            help="Glob patterns to match files to delete. Based on fnmatch, '*' matches files recursively.",
        ),
    ],
    repo_type: RepoTypeOpt = RepoType.model,
    revision: RevisionOpt = None,
    commit_message: Annotated[
        str | None,
        typer.Option(
            help="The summary / title / first line of the generated commit.",
        ),
    ] = None,
    commit_description: Annotated[
        str | None,
        typer.Option(
            help="The description of the generated commit.",
        ),
    ] = None,
    create_pr: Annotated[
        bool,
        typer.Option(
            help="Whether to create a new Pull Request for these changes.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Delete files from a repo on the Hub."""
    api = get_hf_api(token=token)
    url = api.delete_files(
        delete_patterns=patterns,
        repo_id=repo_id,
        repo_type=repo_type.value,
        revision=revision,
        commit_message=commit_message,
        commit_description=commit_description,
        create_pr=create_pr,
    )
    out.result("Files deleted", repo_id=repo_id, commit_url=url)

