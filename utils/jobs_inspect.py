
def jobs_inspect(
    job_ids: Annotated[
        list[str],
        typer.Argument(
            help="Job IDs to inspect (or 'namespace/job_id')",
        ),
    ],
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Display detailed information on one or more Jobs"""
    parsed_ids = []
    for job_id in job_ids:
        job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)
        parsed_ids.append(job_id)
    job_ids = parsed_ids
    api = get_hf_api(token=token)
    jobs = [api.inspect_job(job_id=job_id, namespace=namespace) for job_id in job_ids]
    out.table([_dataclass_to_dict(job) for job in jobs])

