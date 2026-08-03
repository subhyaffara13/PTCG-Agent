from typing import Any

def metadata_eval_result(
    *,
    model_pretty_name: str,
    task_pretty_name: str,
    task_id: str,
    metrics_pretty_name: str,
    metrics_id: str,
    metrics_value: Any,
    dataset_pretty_name: str,
    dataset_id: str,
    metrics_config: str | None = None,
    metrics_verified: bool = False,
    dataset_config: str | None = None,
    dataset_split: str | None = None,
    dataset_revision: str | None = None,
    metrics_verification_token: str | None = None,
) -> dict:
    """
    Creates a metadata dict with the result from a model evaluated on a dataset.

    Args:
        model_pretty_name (`str`):
            The name of the model in natural language.
        task_pretty_name (`str`):
            The name of a task in natural language.
        task_id (`str`):
            Example: automatic-speech-recognition. A task id.
        metrics_pretty_name (`str`):
            A name for the metric in natural language. Example: Test WER.
        metrics_id (`str`):
            Example: wer. A metric id from https://hf.co/metrics.
        metrics_value (`Any`):
            The value from the metric. Example: 20.0 or "20.0 ± 1.2".
        dataset_pretty_name (`str`):
            The name of the dataset in natural language.
        dataset_id (`str`):
            Example: common_voice. A dataset id from https://hf.co/datasets.
        metrics_config (`str`, *optional*):
            The name of the metric configuration used in `load_metric()`.
            Example: bleurt-large-512 in `load_metric("bleurt", "bleurt-large-512")`.
        metrics_verified (`bool`, *optional*, defaults to `False`):
            Indicates whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not. Automatically computed by Hugging Face, do not set.
        dataset_config (`str`, *optional*):
            Example: fr. The name of the dataset configuration used in `load_dataset()`.
        dataset_split (`str`, *optional*):
            Example: test. The name of the dataset split used in `load_dataset()`.
        dataset_revision (`str`, *optional*):
            Example: 5503434ddd753f426f4b38109466949a1217c2bb. The name of the dataset dataset revision
            used in `load_dataset()`.
        metrics_verification_token (`bool`, *optional*):
            A JSON Web Token that is used to verify whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not.

    Returns:
        `dict`: a metadata dict with the result from a model evaluated on a dataset.

    Example:
        ```python
        >>> from huggingface_hub import metadata_eval_result
        >>> results = metadata_eval_result(
        ...         model_pretty_name="RoBERTa fine-tuned on ReactionGIF",
        ...         task_pretty_name="Text Classification",
        ...         task_id="text-classification",
        ...         metrics_pretty_name="Accuracy",
        ...         metrics_id="accuracy",
        ...         metrics_value=0.2662102282047272,
        ...         dataset_pretty_name="ReactionJPEG",
        ...         dataset_id="julien-c/reactionjpeg",
        ...         dataset_config="default",
        ...         dataset_split="test",
        ... )
        >>> results == {
        ...     'model-index': [
        ...         {
        ...             'name': 'RoBERTa fine-tuned on ReactionGIF',
        ...             'results': [
        ...                 {
        ...                     'task': {
        ...                         'type': 'text-classification',
        ...                         'name': 'Text Classification'
        ...                     },
        ...                     'dataset': {
        ...                         'name': 'ReactionJPEG',
        ...                         'type': 'julien-c/reactionjpeg',
        ...                         'config': 'default',
        ...                         'split': 'test'
        ...                     },
        ...                     'metrics': [
        ...                         {
        ...                             'type': 'accuracy',
        ...                             'value': 0.2662102282047272,
        ...                             'name': 'Accuracy',
        ...                             'verified': False
        ...                         }
        ...                     ]
        ...                 }
        ...             ]
        ...         }
        ...     ]
        ... }
        True

        ```
    """

    return {
        "model-index": eval_results_to_model_index(
            model_name=model_pretty_name,
            eval_results=[
                EvalResult(
                    task_name=task_pretty_name,
                    task_type=task_id,
                    metric_name=metrics_pretty_name,
                    metric_type=metrics_id,
                    metric_value=metrics_value,
                    dataset_name=dataset_pretty_name,
                    dataset_type=dataset_id,
                    metric_config=metrics_config,
                    verified=metrics_verified,
                    verify_token=metrics_verification_token,
                    dataset_config=dataset_config,
                    dataset_split=dataset_split,
                    dataset_revision=dataset_revision,
                )
            ],
        )
    }

