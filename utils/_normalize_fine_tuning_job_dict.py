
def _normalize_fine_tuning_job_dict(
    data: Dict[str, Any], is_azure: bool = False
) -> Dict[str, Any]:
    """
    Normalize Azure OpenAI FineTuningJob response to match OpenAI schema.

    Azure differences:
    - organization_id: null → ""
    - result_files: null → []
    - status: mapped via _AZURE_STATUS_MAP
    """
    if not is_azure:
        return data

    normalized = data.copy()

    if normalized.get("organization_id") is None:
        normalized["organization_id"] = ""

    if normalized.get("result_files") is None:
        normalized["result_files"] = []

    status = normalized.get("status")
    if status in _AZURE_STATUS_MAP:
        normalized["status"] = _AZURE_STATUS_MAP[status]

    return normalized

