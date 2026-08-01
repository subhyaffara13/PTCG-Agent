
def branch_create(
    repo_id: RepoIdArg,
    branch: Annotated[
        str,
        typer.Argument(
            help="The name of the branch to create.",
        ),
    ],
    revision: RevisionOpt = None,
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
    exist_ok: Annotated[
        bool,
        typer.Option(
            help="If set to True, do not raise an error if branch already exists.",
        ),
    ] = False,
) -> None:
    """Create a new branch for a repo on the Hub."""
    api = get_hf_api(token=token)
    api.create_branch(
        repo_id=repo_id,
        branch=branch,
        revision=revision,
        repo_type=repo_type.value,
        exist_ok=exist_ok,
    )
    out.result("Branch created", branch=branch, repo_type=repo_type.value, repo_id=repo_id)

