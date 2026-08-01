
def _extract_job_id_from_arn(arn: str) -> Optional[str]:
    """``arn:aws:bedrock:<region>:<acct>:model-invocation-job/<job-id>`` -> ``<job-id>``."""
    if ":model-invocation-job/" not in arn:
        return None
    return arn.rsplit("/", 1)[-1] or None

