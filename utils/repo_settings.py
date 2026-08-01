
def repo_settings(
    repo_id: RepoIdArg,
    gated: Annotated[
        GatedChoices | None,
        typer.Option(
            help="The gated status for the repository.",
        ),
    ] = None,
    private: PrivateOpt = None,
    public: PublicOpt = None,
    protected: ProtectedOpt = None,
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
) -> None:
    """Update the settings of a repository."""
    api = get_hf_api(token=token)
    api.update_repo_settings(
        repo_id=repo_id,
        gated=(None if gated is None else False if gated is GatedChoices.false else gated.value),
        visibility="private" if private else "public" if public else "protected" if protected else None,  # type: ignore [arg-type]
        repo_type=repo_type.value,
    )
    out.result("Repo settings updated", repo_id=repo_id)

