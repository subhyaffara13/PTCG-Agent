from typing import Callable, List, Optional, Union

def get_dynamic_callbacks(
    dynamic_callbacks: Optional[List[Union[str, Callable, "CustomLogger"]]],
) -> List:
    returned_callbacks = litellm.callbacks.copy()
    if dynamic_callbacks:
        returned_callbacks.extend(dynamic_callbacks)  # type: ignore
    return returned_callbacks

