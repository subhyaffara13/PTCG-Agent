
def eval_results_to_model_index(model_name: str, eval_results: list[EvalResult]) -> list[dict[str, Any]]:
    """Takes in given model name and list of `huggingface_hub.EvalResult` and returns a
    valid model-index that will be compatible with the format expected by the
    Hugging Face Hub.

    Args:
        model_name (`str`):
            Name of the model (ex. "my-cool-model"). This is used as the identifier
            for the model on leaderboards like PapersWithCode.
        eval_results (`list[EvalResult]`):
            List of `huggingface_hub.EvalResult` objects containing the metrics to be
            reported in the model-index.

    Returns:
        model_index (`list[dict[str, Any]]`): The eval_results converted to a model-index.

    Example:
        ```python
        >>> from huggingface_hub.repocard_data import eval_results_to_model_index, EvalResult
        >>> # Define minimal eval_results
        >>> eval_results = [
        ...     EvalResult(
        ...         task_type="image-classification",  # Required
        ...         dataset_type="beans",  # Required
        ...         dataset_name="Beans",  # Required
        ...         metric_type="accuracy",  # Required
        ...         metric_value=0.9,  # Required
        ...     )
        ... ]
        >>> eval_results_to_model_index("my-cool-model", eval_results)
        [{'name': 'my-cool-model', 'results': [{'task': {'type': 'image-classification'}, 'dataset': {'name': 'Beans', 'type': 'beans'}, 'metrics': [{'type': 'accuracy', 'value': 0.9}]}]}]

        ```
    """

    # Metrics are reported on a unique task-and-dataset basis.
    # Here, we make a map of those pairs and the associated EvalResults.
    task_and_ds_types_map: dict[Any, list[EvalResult]] = defaultdict(list)
    for eval_result in eval_results:
        task_and_ds_types_map[eval_result.unique_identifier].append(eval_result)

    # Use the map from above to generate the model index data.
    model_index_data: list[dict[str, Any]] = []
    for results in task_and_ds_types_map.values():
        # All items from `results` share same metadata
        sample_result = results[0]
        data: dict[str, Any] = {
            "task": {
                "type": sample_result.task_type,
                "name": sample_result.task_name,
            },
            "dataset": {
                "name": sample_result.dataset_name,
                "type": sample_result.dataset_type,
                "config": sample_result.dataset_config,
                "split": sample_result.dataset_split,
                "revision": sample_result.dataset_revision,
                "args": sample_result.dataset_args,
            },
            "metrics": [
                {
                    "type": result.metric_type,
                    "value": result.metric_value,
                    "name": result.metric_name,
                    "config": result.metric_config,
                    "args": result.metric_args,
                    "verified": result.verified,
                    "verifyToken": result.verify_token,
                }
                for result in results
            ],
        }
        if sample_result.source_url is not None:
            source: dict[str, str] = {
                "url": sample_result.source_url,
            }
            if sample_result.source_name is not None:
                source["name"] = sample_result.source_name
            data["source"] = source
        model_index_data.append(data)

    # TODO - Check if there cases where this list is longer than one?
    # Finally, the model index itself is list of dicts.
    model_index = [
        {
            "name": model_name,
            "results": model_index_data,
        }
    ]
    return _remove_none(model_index)

