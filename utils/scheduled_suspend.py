
def scheduled_suspend(
    scheduled_job_id: ScheduledJobIdArg,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Suspend (pause) a scheduled Job."""
    scheduled_job_id, namespace = _parse_namespace_from_job_id(scheduled_job_id, namespace)
    api = get_hf_api(token=token)
    api.suspend_scheduled_job(scheduled_job_id=scheduled_job_id, namespace=namespace)
    out.result("Scheduled Job suspended", id=scheduled_job_id)
    out.hint(f"Use `hf jobs scheduled resume {scheduled_job_id}` to resume it.")

