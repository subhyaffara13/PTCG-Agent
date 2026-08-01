
def discussion_list(
    repo_id: RepoIdArg,
    status: Annotated[
        DiscussionStatus,
        typer.Option(
            "-s",
            "--status",
            help="Filter by status (open, closed, merged, draft, all).",
        ),
    ] = DiscussionStatus.open,
    kind: Annotated[
        DiscussionKind,
        typer.Option(
            "-k",
            "--kind",
            help="Filter by kind (discussion, pull_request, all).",
        ),
    ] = DiscussionKind.all,
    author: AuthorOpt = None,
    limit: LimitOpt = 30,
    repo_type: RepoTypeOpt = RepoType.model,
    token: TokenOpt = None,
) -> None:
    """List discussions and pull requests on a repo."""
    api = get_hf_api(token=token)

    api_status: constants.DiscussionStatusFilter | None
    if status == DiscussionStatus.open:
        api_status = "open"
    elif status == DiscussionStatus.closed:
        api_status = "closed"
    else:
        api_status = None

    api_discussion_type: constants.DiscussionTypeFilter | None
    if kind == DiscussionKind.all:
        api_discussion_type = None
    else:
        api_discussion_type = kind.value  # type: ignore[assignment]

    discussions = []
    for d in api.get_repo_discussions(
        repo_id=repo_id,
        author=author,
        discussion_type=api_discussion_type,
        discussion_status=api_status,
        repo_type=repo_type.value,
    ):
        if status.value in _CLIENT_SIDE_STATUSES and d.status != status.value:
            continue
        discussions.append(d)
        if len(discussions) >= limit:
            break

    items = [_dataclass_to_dict(d) for d in discussions]
    out.table(
        items,
        headers=["num", "title", "is_pull_request", "status", "author", "created_at"],
        id_key="num",
    )

