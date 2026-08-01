
def _is_potential_model_name_in_model_cost(
    potential_model_names: PotentialModelNamesAndCustomLLMProvider,
) -> bool:
    """
    Check if the potential model name is in the model cost (case-insensitive).
    """
    return any(
        _get_model_cost_key(str(potential_model_name)) is not None
        for potential_model_name in potential_model_names.values()
    )

