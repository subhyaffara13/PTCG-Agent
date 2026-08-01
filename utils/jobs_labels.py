
def jobs_labels(
    job_id: JobIdArg,
    label: LabelsOpt = None,
    clear: Annotated[bool, typer.Option("--clear", help="Remove all labels from the job.")] = False,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Update labels on a Job. Replaces all existing labels."""
    if not label and not clear:
        raise CLIError("Please set at least one label with --label. To remove all labels, pass --clear.")
    if label and clear:
        raise CLIError(
            "Cannot set labels and clear them at the same time. Please use either --label or --clear, not both."
        )
    job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)
    labels = _parse_labels_map(label) or {}
    api = get_hf_api(token=token)
    job = api.update_job_labels(job_id=job_id, labels=labels, namespace=namespace)
    out.result("Labels updated", id=job.id)

