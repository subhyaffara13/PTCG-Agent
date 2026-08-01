
def parse_eval_result_entries(data: list[dict[str, Any]]) -> list[EvalResultEntry]:
    """Parse a list of dicts into [`EvalResultEntry`] objects.

    This parses the `.eval_results/*.yaml` format. For the legacy `model-index` format,
    use [`model_index_to_eval_results`] instead.

    Args:
        data (`list[dict[str, Any]]`):
            A list of dictionaries (e.g., parsed from YAML or API response).

    Returns:
        `list[EvalResultEntry]`: A list of evaluation result entry objects.

    Example:
        ```python
        >>> from huggingface_hub import parse_eval_result_entries
        >>> data = [
        ...     {"dataset": {"id": "cais/hle", "task_id": "default"}, "value": 20.90},
        ...     {"dataset": {"id": "Idavidrein/gpqa", "task_id": "gpqa_diamond"}, "value": 0.412},
        ... ]
        >>> entries = parse_eval_result_entries(data)
        >>> entries[0].dataset_id
        'cais/hle'
        >>> entries[0].value
        20.9

        ```
    """
    entries = []
    for item in data:
        entry_data = item.get("data", item)
        dataset = entry_data.get("dataset", {})
        source = entry_data.get("source", {})
        entry = EvalResultEntry(
            dataset_id=dataset["id"],
            value=entry_data["value"],
            task_id=dataset["task_id"],
            dataset_revision=dataset.get("revision"),
            verify_token=entry_data.get("verifyToken"),
            date=entry_data.get("date"),
            source_url=source.get("url") if source else None,
            source_name=source.get("name") if source else None,
            source_user=source.get("user") if source else None,
            source_org=source.get("org") if source else None,
            notes=entry_data.get("notes"),
        )
        entries.append(entry)
    return entries

