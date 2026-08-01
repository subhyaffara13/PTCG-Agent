
def scheduled_uv_run(
    schedule: ScheduleArg,
    script: ScriptArg,
    script_args: ScriptArgsArg = None,
    suspend: SuspendOpt = None,
    concurrency: ConcurrencyOpt = None,
    image: ImageOpt = None,
    flavor: FlavorOpt = None,
    env: EnvOpt = None,
    secrets: SecretsOpt = None,
    label: LabelsOpt = None,
    volume: VolumesOpt = None,
    env_file: EnvFileOpt = None,
    secrets_file: SecretsFileOpt = None,
    timeout: TimeoutOpt = None,
    expose: ExposeOpt = None,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
    with_: WithOpt = None,
    python: PythonOpt = None,
) -> None:
    """Run a UV script (local file or URL) on HF infrastructure"""
    env_map = parse_env_map(env, env_file)
    secrets_map = parse_env_map(secrets, secrets_file)

    api = get_hf_api(token=token)
    job = api.create_scheduled_uv_job(
        script=script,
        script_args=script_args or [],
        schedule=schedule,
        suspend=suspend,
        concurrency=concurrency,
        dependencies=with_,
        python=python,
        image=image,
        env=env_map,
        secrets=secrets_map,
        labels=_parse_labels_map(label),
        volumes=parse_volumes(volume),
        flavor=flavor,
        timeout=timeout,
        expose=expose,
        namespace=namespace,
    )
    out.result("Scheduled Job created", id=job.id)
    out.hint(f"Use `hf jobs scheduled inspect {job.id}` to view its details.")

