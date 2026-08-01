
def discussion_merge(
    repo_id: RepoIdArg,
    num: DiscussionNumArg,
    comment: Annotated[
        str | None,
        typer.Option(
            "--comment",
            help="An optional comment to post when merging.",
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
    """Merge a pull request."""
    out.confirm(f"Merge #{num} on '{repo_id}'?", yes=yes)
    api = get_hf_api(token=token)
    api.merge_pull_request(
        repo_id=repo_id,
        discussion_num=num,
        comment=comment,
        repo_type=repo_type.value,
    )
    out.result(f"Merged #{num} in {repo_id}", num=num, repo=repo_id)

