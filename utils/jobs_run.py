
def jobs_run(
    image: ImageArg,
    command: CommandArg,
    env: EnvOpt = None,
    secrets: SecretsOpt = None,
    label: LabelsOpt = None,
    volume: VolumesOpt = None,
    env_file: EnvFileOpt = None,
    secrets_file: SecretsFileOpt = None,
    flavor: FlavorOpt = None,
    timeout: TimeoutOpt = None,
    detach: DetachOpt = False,
    expose: ExposeOpt = None,
    ssh: SshEnabledOpt = False,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Run a Job."""
    env_map = parse_env_map(env, env_file)
    secrets_map = parse_env_map(secrets, secrets_file)

    api = get_hf_api(token=token)
    job = api.run_job(
        image=image,
        command=command,
        env=env_map,
        secrets=secrets_map,
        labels=_parse_labels_map(label),
        volumes=parse_volumes(volume),
        flavor=flavor,
        timeout=timeout,
        expose=expose,
        ssh=ssh,
        namespace=namespace,
    )
    out.result("Job started", id=job.id, url=job.url)
    if isinstance(job.status.expose_urls, list):
        urls = "\n".join(f"  {url}" for url in job.status.expose_urls)
        out.hint(f"Exposed ports are reachable at (requires an HF token with read access to the job):\n{urls}")
    if isinstance(job.status.ssh_url, str):
        out.hint(f"Use `hf jobs ssh {job.owner.name}/{job.id}` to open an SSH session into the job.")
    if detach:
        job_ref = f"{job.owner.name}/{job.id}"
        out.hint(f"Use `hf jobs logs -f {job_ref}` to stream logs, or `hf jobs inspect {job_ref}` to check status.")
        return
    _stream_logs_and_check_status(api, job)

