from typing import Any

def eval_result_entries_to_yaml(entries: list[EvalResultEntry]) -> list[dict[str, Any]]:
    """Convert a list of [`EvalResultEntry`] objects to a YAML-serializable list of dicts.

    This produces the format expected in `.eval_results/*.yaml` files.

    Args:
        entries (`list[EvalResultEntry]`):
            List of evaluation result entries to serialize.

    Returns:
        `list[dict[str, Any]]`: A list of dictionaries ready to be dumped to YAML.

    Example:
        ```python
        >>> from huggingface_hub import EvalResultEntry, eval_result_entries_to_yaml
        >>> entries = [
        ...     EvalResultEntry(dataset_id="cais/hle", task_id="default", value=20.90),
        ...     EvalResultEntry(dataset_id="Idavidrein/gpqa", task_id="gpqa_diamond", value=0.412),
        ... ]
        >>> yaml_data = eval_result_entries_to_yaml(entries)
        >>> yaml_data[0]
        {'dataset': {'id': 'cais/hle', 'task_id': 'default'}, 'value': 20.9}

        ```

        To upload eval results to the Hub:
        ```python
        >>> import yaml
        >>> from huggingface_hub import upload_file, EvalResultEntry, eval_result_entries_to_yaml
        >>> entries = [
        ...     EvalResultEntry(dataset_id="cais/hle", task_id="default", value=20.90),
        ... ]
        >>> yaml_content = yaml.dump(eval_result_entries_to_yaml(entries))
        >>> upload_file(
        ...     path_or_fileobj=yaml_content.encode(),
        ...     path_in_repo=".eval_results/hle.yaml",
        ...     repo_id="your-username/your-model",
        ... )

        ```
    """
    result = []
    for entry in entries:
        # build the dataset object
        dataset: dict[str, Any] = {"id": entry.dataset_id, "task_id": entry.task_id}
        if entry.dataset_revision is not None:
            dataset["revision"] = entry.dataset_revision

        data: dict[str, Any] = {"dataset": dataset, "value": entry.value}
        if entry.verify_token is not None:
            data["verifyToken"] = entry.verify_token
        if entry.date is not None:
            data["date"] = entry.date
        # build the source object
        if entry.source_url is not None:
            source: dict[str, Any] = {"url": entry.source_url}
            if entry.source_name is not None:
                source["name"] = entry.source_name
            if entry.source_user is not None:
                source["user"] = entry.source_user
            if entry.source_org is not None:
                source["org"] = entry.source_org
            data["source"] = source
        if entry.notes is not None:
            data["notes"] = entry.notes

        result.append(data)
    return result

