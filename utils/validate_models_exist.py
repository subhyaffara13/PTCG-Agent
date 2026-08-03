from typing import List, Tuple

def validate_models_exist(model_names: List[str], llm_router) -> Tuple[bool, List[str]]:
    """
    Validate that all requested model names exist in the router.
    Checks only exact model name matches.

    Returns:
        Tuple[bool, List[str]]: (all_valid, missing_models)
    """
    if llm_router is None:
        return False, model_names

    router_model_names = set(llm_router.get_model_names())
    missing = [m for m in model_names if m not in router_model_names]
    return (len(missing) == 0, missing)

