
def branch_delete(
    repo_id: RepoIdArg,
    branch: Annotated[
        str,
        typer.Argument(
            help="The name of the branch to delete.",
        ),
    ],
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
) -> None:
    """Delete a branch from a repo on the Hub."""
    api = get_hf_api(token=token)
    api.delete_branch(
        repo_id=repo_id,
        branch=branch,
        repo_type=repo_type.value,
    )
    out.result("Branch deleted", branch=branch, repo_type=repo_type.value, repo_id=repo_id)

