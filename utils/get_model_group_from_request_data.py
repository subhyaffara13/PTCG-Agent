
def get_model_group_from_request_data(data: dict) -> Optional[str]:
    _metadata = data.get("metadata", None) or {}
    _model_group = _metadata.get("model_group", None)
    if _model_group is not None:
        return _model_group

    return None

