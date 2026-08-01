
def jobs_wait(
    job_ids: Annotated[
        list[str],
        typer.Argument(
            help="Job IDs to wait for (or 'namespace/job_id').",
        ),
    ],
    timeout: Annotated[
        str | None,
        typer.Option(
            help="Max time to wait: int/float with s (seconds, default), m (minutes), h (hours) or d (days).",
        ),
    ] = None,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Wait for one or more Jobs to reach a terminal state.

    Blocks until every Job has finished, then exits with code 0 if all Jobs completed
    successfully, or a non-zero exit code if any Job was canceled, errored or deleted.

    All Jobs must belong to the same namespace.
    """
    parsed_ids = []
    namespaces = set()
    for job_id in job_ids:
        parsed_id, parsed_namespace = _parse_namespace_from_job_id(job_id, namespace)
        parsed_ids.append(parsed_id)
        namespaces.add(parsed_namespace)
    if len(namespaces) > 1:
        raise CLIError(
            "All Job IDs must be in the same namespace, got: "
            + ", ".join(str(ns) for ns in sorted(namespaces, key=str))
        )
    namespace = namespaces.pop()
    timeout_secs = parse_duration(timeout) if timeout is not None else None

    api = get_hf_api(token=token)
    status = out.status(f"Waiting for {len(parsed_ids)} Job(s) to finish...")
    try:
        jobs = api.wait_for_job(parsed_ids, timeout=timeout_secs, namespace=namespace)
    except TimeoutError:
        status.done("Timed out.")
        raise CLIError(f"Timed out after {timeout} waiting for Job(s) to finish.") from None
    status.done(f"{len(jobs)} Job(s) finished.")

    out.table([{"id": job.id, "stage": str(job.status.stage), "message": job.status.message} for job in jobs])
    failed = [job for job in jobs if job.status.stage != JobStage.COMPLETED]
    if failed:
        raise CLIError(
            f"{len(failed)} of {len(jobs)} Job(s) did not complete successfully: "
            + ", ".join(f"{job.id} ({job.status.stage})" for job in failed)
        )

