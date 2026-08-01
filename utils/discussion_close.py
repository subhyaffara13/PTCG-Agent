
def discussion_close(
    repo_id: RepoIdArg,
    num: DiscussionNumArg,
    comment: Annotated[
        str | None,
        typer.Option(
            "--comment",
            help="An optional comment to post when closing.",
        ),
    ] = None,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Skip confirmation prompt.",
        ),
    ] = False,
    repo_type: RepoTypeOpt = RepoType.model,
    token: TokenOpt = None,
) -> None:
    """Close a discussion or pull request."""
    out.confirm(f"Close #{num} on '{repo_id}'?", yes=yes)
    api = get_hf_api(token=token)
    api.change_discussion_status(
        repo_id=repo_id,
        discussion_num=num,
        new_status="closed",
        comment=comment,
        repo_type=repo_type.value,
    )
    out.result(f"Closed #{num} in {repo_id}", num=num, repo=repo_id)

