
def tag_list(
    repo_id: RepoIdArg,
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
) -> None:
    """List tags for a repo."""
    repo_type_str = repo_type.value
    api = get_hf_api(token=token)
    try:
        refs = api.list_repo_refs(repo_id=repo_id, repo_type=repo_type_str)
    except RepositoryNotFoundError as e:
        raise CLIError(f"{repo_type_str.capitalize()} '{repo_id}' not found.") from e
    items = [{"name": t.name, "target_commit": t.target_commit, "ref": t.ref} for t in refs.tags]
    out.table(items)

