
def repo_move(
    from_id: RepoIdArg,
    to_id: RepoIdArg,
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
) -> None:
    """Move a repository from a namespace to another namespace."""
    api = get_hf_api(token=token)
    api.move_repo(
        from_id=from_id,
        to_id=to_id,
        repo_type=repo_type.value,
    )
    out.result("Repo moved", from_id=from_id, to_id=to_id)

