from typing import Optional

def is_known_model(model: Optional[str], llm_router: Optional[Router]) -> bool:
    """
    Returns True if the model is in the llm_router model names
    """
    if model is None or llm_router is None:
        return False
    model_names = llm_router.get_model_names()

    model_names_set = set(model_names)

    is_in_list = False
    if model in model_names_set:
        is_in_list = True

    return is_in_list

