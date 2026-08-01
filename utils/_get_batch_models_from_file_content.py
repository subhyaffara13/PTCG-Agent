
def _get_batch_models_from_file_content(
    file_content_dictionary: List[dict],
    model_name: Optional[str] = None,
) -> List[str]:
    """
    Get the models from the file content
    """
    if model_name:
        return [model_name]
    batch_models = []
    for _item in file_content_dictionary:
        if _batch_response_was_successful(_item):
            _response_body = _get_response_from_batch_job_output_file(_item)
            _model = _response_body.get("model")
            if _model:
                batch_models.append(_model)
    return batch_models

