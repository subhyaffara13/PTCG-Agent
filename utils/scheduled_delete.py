
def scheduled_delete(
    scheduled_job_id: ScheduledJobIdArg,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Delete a scheduled Job."""
    scheduled_job_id, namespace = _parse_namespace_from_job_id(scheduled_job_id, namespace)
    api = get_hf_api(token=token)
    api.delete_scheduled_job(scheduled_job_id=scheduled_job_id, namespace=namespace)
    out.result("Scheduled Job deleted", id=scheduled_job_id)

