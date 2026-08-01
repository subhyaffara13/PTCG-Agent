
def _parse_namespace_from_job_id(job_id: str, namespace: str | None) -> tuple[str, str | None]:
    """Extract namespace from job_id if provided in 'namespace/job_id' format.

    Allows users to pass job IDs copied from the Hub UI (e.g. 'username/job_id')
    instead of only bare job IDs. If the namespace is also provided explicitly via
    --namespace and conflicts, a CLIError is raised.
    """
    if not job_id:
        raise CLIError("Job ID cannot be empty.")

    if job_id.count("/") > 1:
        raise CLIError(f"Job ID must be in the form 'job_id' or 'namespace/job_id': '{job_id}'.")

    if "/" not in job_id:
        return job_id, namespace

    extracted_namespace, parsed_job_id = job_id.split("/", 1)
    if not extracted_namespace or not parsed_job_id:
        raise CLIError(f"Job ID must be in the form 'job_id' or 'namespace/job_id': '{job_id}'.")

    if namespace is not None and namespace != extracted_namespace:
        raise CLIError(
            f"Conflicting namespace: got --namespace='{namespace}' but job ID implies namespace='{extracted_namespace}'"
        )

    return parsed_job_id, extracted_namespace

