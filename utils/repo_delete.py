
def repo_delete(
    repo_id: RepoIdArg,
    repo_type: RepoTypeOpt = RepoType.model,
    token: TokenOpt = None,
    missing_ok: Annotated[
        bool,
        typer.Option(
            help="If set to True, do not raise an error if repo does not exist.",
        ),
    ] = False,
    yes: Annotated[
        bool,
        typer.Option(
            "-y",
            "--yes",
            help="Answer Yes to prompt automatically.",
        ),
    ] = False,
) -> None:
    """Delete a repo from the Hub. This is an irreversible operation."""
    out.confirm(f"You are about to permanently delete {repo_type.value} '{repo_id}'. Proceed?", yes=yes)
    api = get_hf_api(token=token)
    api.delete_repo(
        repo_id=repo_id,
        repo_type=repo_type.value,
        missing_ok=missing_ok,
    )
    out.result("Repo deleted", repo_id=repo_id)

