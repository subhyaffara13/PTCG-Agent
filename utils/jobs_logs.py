
def jobs_logs(
    job_id: JobIdArg,
    follow: Annotated[
        bool,
        typer.Option(
            "-f",
            "--follow",
            help="Follow log output (stream until the job completes). Without this flag, only currently available logs are printed.",
        ),
    ] = False,
    tail: Annotated[
        int | None,
        typer.Option(
            "-n",
            "--tail",
            help="Number of lines to show from the end of the logs. When combined with --follow, starts streaming from the last N lines.",
        ),
    ] = None,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Fetch the logs of a Job.

    By default, prints currently available logs and exits (non-blocking).
    Use --follow/-f to stream logs in real-time until the job completes.
    Use --tail/-n to limit the number of lines returned (server-side when supported).

    Note: following exits when the log stream ends, regardless of whether the Job
    succeeded or failed. Run `hf jobs inspect <job_id>` to check the final status.
    """
    job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)

    api = get_hf_api(token=token)
    logs = api.fetch_job_logs(job_id=job_id, namespace=namespace, follow=follow, tail=tail)
    for log in logs:
        out.text(log)
    if follow:
        job_ref = f"{namespace}/{job_id}" if namespace else job_id
        out.hint(f"Stream ended. Run `hf jobs inspect {job_ref}` to check the final status (e.g. COMPLETED or ERROR).")

