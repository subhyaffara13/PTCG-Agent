
def scheduled_run(
    schedule: ScheduleArg,
    image: ImageArg,
    command: CommandArg,
    suspend: SuspendOpt = None,
    concurrency: ConcurrencyOpt = None,
    env: EnvOpt = None,
    secrets: SecretsOpt = None,
    label: LabelsOpt = None,
    volume: VolumesOpt = None,
    env_file: EnvFileOpt = None,
    secrets_file: SecretsFileOpt = None,
    flavor: FlavorOpt = None,
    timeout: TimeoutOpt = None,
    expose: ExposeOpt = None,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Schedule a Job."""
    env_map = parse_env_map(env, env_file)
    secrets_map = parse_env_map(secrets, secrets_file)

    api = get_hf_api(token=token)
    scheduled_job = api.create_scheduled_job(
        image=image,
        command=command,
        schedule=schedule,
        suspend=suspend,
        concurrency=concurrency,
        env=env_map,
        secrets=secrets_map,
        labels=_parse_labels_map(label),
        volumes=parse_volumes(volume),
        flavor=flavor,
        timeout=timeout,
        expose=expose,
        namespace=namespace,
    )
    out.result("Scheduled Job created", id=scheduled_job.id)
    out.hint(f"Use `hf jobs scheduled inspect {scheduled_job.id}` to view its details.")

