
def jobs_ssh(
    job_id: JobIdArg,
    identity_file: SshIdentityFileOpt = None,
    dry_run: SshDryRunOpt = False,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """SSH into a running Job.

    If the Job is not yet running, waits until it reaches the RUNNING state before
    connecting. Requires the Job to be started with SSH enabled (`hf jobs run --ssh ...`)
    and your SSH public key to be registered at https://huggingface.co/settings/keys.
    """
    job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)
    api = get_hf_api(token=token)
    job = api.inspect_job(job_id=job_id, namespace=namespace)
    if job.status.ssh_url is None:
        raise CLIError("SSH is not enabled on this job. Start a job with SSH support using `hf jobs run --ssh ...`.")
    if job.status.stage in TERMINAL_JOB_STAGES:
        raise CLIError(f"Cannot SSH into job '{job.id}': job has already finished (stage: '{job.status.stage}').")
    if job.status.stage != JobStage.RUNNING:
        status = out.status(f"Waiting for job '{job.id}' to be running (stage: '{job.status.stage}')...")
        job = api.wait_for_job(job_id=job.id, namespace=namespace, stages=[JobStage.RUNNING])
        if job.status.stage != JobStage.RUNNING:
            status.done("Job finished.")
            raise CLIError(
                f"Cannot SSH into job '{job.id}': job finished before reaching RUNNING (stage: '{job.status.stage}')."
            )
        status.done("Job is running.")
    ssh_url = urlsplit(job.status.ssh_url)
    exec_ssh(
        f"{ssh_url.username}@{ssh_url.hostname}",  # type: ignore
        port=ssh_url.port,
        identity_file=identity_file,
        dry_run=dry_run,
    )

