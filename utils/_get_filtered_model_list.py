import re

def _get_filtered_model_list(
    model_list, only_models_matching_regex, only_access_groups_matching_regex
):
    """Return a list of models that pass the filter criteria."""
    model_regex = (
        re.compile(only_models_matching_regex) if only_models_matching_regex else None
    )
    access_group_regex = (
        re.compile(only_access_groups_matching_regex)
        if only_access_groups_matching_regex
        else None
    )
    return [
        model
        for model in model_list
        if _filter_model(model, model_regex, access_group_regex)
    ]

