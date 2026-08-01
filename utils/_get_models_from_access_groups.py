
def _get_models_from_access_groups(
    model_access_groups: Dict[str, List[str]],
    all_models: List[str],
    include_model_access_groups: Optional[bool] = False,
) -> List[str]:
    idx_to_remove = []
    new_models = []
    for idx, model in enumerate(all_models):
        if model in model_access_groups:
            if (
                not include_model_access_groups
            ):  # remove access group, unless requested - e.g. when creating a key
                idx_to_remove.append(idx)
            new_models.extend(model_access_groups[model])

    for idx in sorted(idx_to_remove, reverse=True):
        all_models.pop(idx)

    all_models.extend(new_models)
    return all_models

