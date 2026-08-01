
def _get_model_info_obj_from_yaml(model: dict[str, Any]) -> ModelYamlInfo:
    """Extract model info from a model dict and return as ModelYamlInfo dataclass."""
    model_name: str = model["model_name"]
    model_params: dict[str, Any] = model["litellm_params"]
    model_info: dict[str, Any] = model.get("model_info", {})
    model_id: str = model_params["model"]
    access_groups = model_info.get("access_groups", [])
    provider = model_id.split("/", 1)[0] if "/" in model_id else model_id
    return ModelYamlInfo(
        model_name=model_name,
        model_params=model_params,
        model_info=model_info,
        model_id=model_id,
        access_groups=access_groups,
        provider=provider,
    )

