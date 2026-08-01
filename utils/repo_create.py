
def repo_create(
    repo_id: RepoIdArg,
    repo_type: RepoTypeOpt = RepoType.model,
    space_sdk: Annotated[
        str | None,
        typer.Option(
            help="Hugging Face Spaces SDK type. Required when --type is set to 'space'.",
        ),
    ] = None,
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
    resource_group_id: Annotated[
        str | None,
        typer.Option(
            help="Resource group in which to create the repo. Resource groups is only available for Enterprise Hub organizations.",
        ),
    ] = None,
    region: Annotated[
        REPO_REGIONS | None,
        typer.Option(
            "--region",
            help="Cloud region in which to create the repo. Can be one of 'us' or 'eu'. Requires Team plan or above.",
        ),
    ] = None,
    hardware: SpaceHardwareOpt = None,
    storage: SpaceStorageOpt = None,
    sleep_time: SpaceSleepTimeOpt = None,
    secrets: SecretsOpt = None,
    secrets_file: SecretsFileOpt = None,
    env: EnvOpt = None,
    env_file: EnvFileOpt = None,
    volume: VolumesOpt = None,
) -> None:
    """Create a new repo on the Hub."""
    api = get_hf_api(token=token)
    repo_url = api.create_repo(
        repo_id=repo_id,
        repo_type=repo_type.value,
        visibility="private" if private else "public" if public else "protected" if protected else None,  # type: ignore [arg-type]
        token=token,
        exist_ok=exist_ok,
        resource_group_id=resource_group_id,
        region=region,
        space_sdk=space_sdk,
        space_hardware=hardware,
        space_storage=storage,
        space_sleep_time=sleep_time,
        space_secrets=env_map_to_key_value_list(parse_env_map(secrets, secrets_file)),
        space_variables=env_map_to_key_value_list(parse_env_map(env, env_file)),
        space_volumes=parse_volumes(volume),
    )
    out.result("Repo created", repo_id=repo_url.repo_id, url=str(repo_url))

