from typing import Any

def _get_bound_node(model: ObjectModel) -> Any:
    # TODO: Use isinstance instead of try ... except after _instance has typing
    try:
        return model._instance._proxied
    except AttributeError:
        return model._instance

