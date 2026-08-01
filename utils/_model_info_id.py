
def _model_info_id(model_info: object) -> str | None:
    """The deployment id from a ``metadata.model_info`` sub-dict, if present."""
    if isinstance(model_info, Mapping):
        return as_str(model_info.get("id"))
    return None

