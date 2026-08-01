
def _parse_job_id_from_url(url: str) -> str | None:
    """Extract the job_id from a (scheduled) job API URL, if present."""
    match = _JOB_ID_FROM_URL_REGEX.search(url)
    return match.group(1) if match else None

