
def scheduled_labels(
    scheduled_job_id: ScheduledJobIdArg,
    label: LabelsOpt = None,
    clear: Annotated[bool, typer.Option("--clear", help="Remove all labels from the scheduled job.")] = False,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Update labels on a scheduled Job. Replaces all existing labels."""
    if not label and not clear:
        raise CLIError("Please set at least one label with --label. To remove all labels, pass --clear.")
    if label and clear:
        raise CLIError(
            "Cannot set labels and clear them at the same time. Please use either --label or --clear, not both."
        )
    scheduled_job_id, namespace = _parse_namespace_from_job_id(scheduled_job_id, namespace)
    labels = _parse_labels_map(label) or {}
    api = get_hf_api(token=token)
    scheduled_job = api.update_scheduled_job_labels(
        scheduled_job_id=scheduled_job_id, labels=labels, namespace=namespace
    )
    out.result("Labels updated", id=scheduled_job.id)

