
def jobs_cancel(
    job_id: JobIdArg,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Cancel a Job"""
    job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)
    api = get_hf_api(token=token)
    api.cancel_job(job_id=job_id, namespace=namespace)
    out.result("Job cancelled", id=job_id)

