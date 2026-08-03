from typing import List, Optional, Union

def _get_model_names_for_budget_checks(
    model: Optional[Union[str, List[str]]],
) -> List[str]:
    if model is None:
        return []
    if isinstance(model, str):
        return [model]
    return model

