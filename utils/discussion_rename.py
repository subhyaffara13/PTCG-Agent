
def discussion_rename(
    repo_id: RepoIdArg,
    num: DiscussionNumArg,
    new_title: Annotated[
        str,
        typer.Argument(
            help="The new title.",
        ),
    ],
    repo_type: RepoTypeOpt = RepoType.model,
    token: TokenOpt = None,
) -> None:
    """Rename a discussion or pull request."""
    api = get_hf_api(token=token)
    api.rename_discussion(
        repo_id=repo_id,
        discussion_num=num,
        new_title=new_title,
        repo_type=repo_type.value,
    )
    out.result(f"Renamed #{num} in {repo_id}", num=num, repo=repo_id, title=new_title)

