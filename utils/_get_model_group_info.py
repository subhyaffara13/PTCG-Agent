
def _get_model_group_info(
    llm_router: Router, all_models_str: List[str], model_group: Optional[str]
) -> List[ModelGroupInfoProxy]:
    model_groups: List[ModelGroupInfoProxy] = []

    unique_models = []
    for model in all_models_str:
        if model not in unique_models:
            unique_models.append(model)

    for model in unique_models:
        if model_group is not None and model_group != model:
            continue

        _model_group_info = llm_router.get_model_group_info(model_group=model)

        if _model_group_info is not None:
            model_groups.append(ModelGroupInfoProxy(**_model_group_info.model_dump()))
        else:
            model_group_info = ModelGroupInfoProxy(
                model_group=model,
                providers=[],
            )
            model_groups.append(model_group_info)

    ## check for public model groups
    if litellm.public_model_groups is not None:
        for mg in model_groups:
            if mg.model_group in litellm.public_model_groups:
                mg.is_public_model_group = True

    return model_groups

