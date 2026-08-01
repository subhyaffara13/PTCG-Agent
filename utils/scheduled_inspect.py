
def scheduled_inspect(
    scheduled_job_ids: Annotated[
        list[str],
        typer.Argument(
            help="Scheduled Job IDs to inspect (or 'namespace/scheduled_job_id')",
        ),
    ],
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Display detailed information on one or more scheduled Jobs"""
    parsed_ids = []
    for job_id in scheduled_job_ids:
        job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)
        parsed_ids.append(job_id)
    scheduled_job_ids = parsed_ids
    api = get_hf_api(token=token)
    scheduled_jobs = [
        api.inspect_scheduled_job(scheduled_job_id=scheduled_job_id, namespace=namespace)
        for scheduled_job_id in scheduled_job_ids
    ]
    out.table([_dataclass_to_dict(scheduled_job) for scheduled_job in scheduled_jobs])

