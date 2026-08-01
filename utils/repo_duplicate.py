
def repo_duplicate(
    from_id: RepoIdArg,
    to_id: Annotated[
        str | None,
        typer.Argument(
            help="Destination repo ID (e.g. `myorg/my-copy`). Defaults to your namespace with the same repo name.",
        ),
    ] = None,
    repo_type: RepoTypeOpt = RepoType.model,
    private: PrivateOpt = None,
    public: PublicOpt = None,
    protected: ProtectedOpt = None,
    token: TokenOpt = None,
    exist_ok: Annotated[
        bool,
        typer.Option(
            help="Do not raise an error if repo already exists.",
        ),
    ] = False,
    hardware: SpaceHardwareOpt = None,
    storage: SpaceStorageOpt = None,
    sleep_time: SpaceSleepTimeOpt = None,
    secrets: SecretsOpt = None,
    secrets_file: SecretsFileOpt = None,
    env: EnvOpt = None,
    env_file: EnvFileOpt = None,
    volume: VolumesOpt = None,
) -> None:
    """Duplicate a repo on the Hub (model, dataset, or Space)."""
    api = get_hf_api(token=token)
    repo_url = api.duplicate_repo(
        from_id=from_id,
        to_id=to_id,
        repo_type=repo_type.value,
        visibility="private" if private else "public" if public else "protected" if protected else None,  # type: ignore [arg-type]
        token=token,
        exist_ok=exist_ok,
        space_hardware=hardware,
        space_storage=storage,
        space_sleep_time=sleep_time,
        space_secrets=env_map_to_key_value_list(parse_env_map(secrets, secrets_file)),
        space_variables=env_map_to_key_value_list(parse_env_map(env, env_file)),
        space_volumes=parse_volumes(volume),
    )
    out.result("Repo duplicated", from_id=from_id, to_id=repo_url.repo_id, url=str(repo_url))

