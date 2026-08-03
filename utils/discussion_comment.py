from pathlib import Path


def discussion_comment(
    repo_id: RepoIdArg,
    num: DiscussionNumArg,
    body: Annotated[
        str | None,
        typer.Option(
            "--body",
            help="The comment text (supports Markdown).",
        ),
    ] = None,
    body_file: Annotated[
        Path | None,
        typer.Option(
            "--body-file",
            help="Read the comment from a file. Use '-' for stdin.",
        ),
    ] = None,
    repo_type: RepoTypeOpt = RepoType.model,
    token: TokenOpt = None,
) -> None:
    """Comment on a discussion or pull request."""
    comment = _read_body(body, body_file)
    if comment is None:
        raise typer.BadParameter("Either --body or --body-file is required.")
    api = get_hf_api(token=token)
    api.comment_discussion(
        repo_id=repo_id,
        discussion_num=num,
        comment=comment,
        repo_type=repo_type.value,
    )
    out.result(f"Commented on #{num} in {repo_id}", num=num, repo=repo_id)

