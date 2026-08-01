
def _filter_model(model, model_regex, access_group_regex):
    model_name = model.get("model_name")
    model_params = model.get("litellm_params")
    model_info = model.get("model_info", {})
    if not model_name or not model_params:
        return False
    model_id = model_params.get("model")
    if not model_id or not isinstance(model_id, str):
        return False
    if model_regex and not model_regex.search(model_id):
        return False
    access_groups = model_info.get("access_groups", [])
    if access_group_regex:
        if not isinstance(access_groups, list):
            return False
        if not any(
            isinstance(group, str) and access_group_regex.search(group)
            for group in access_groups
        ):
            return False
    return True

