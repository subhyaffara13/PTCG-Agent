
def _autowrap_check(
    patcher: _Patcher, frame_dict: dict[str, Any], function_ids: set[int]
) -> None:
    """
    Some methods, like `math.sqrt` are common enough we want to automatically wrap them as we see them.
    This method searches a scope for them and patches them if found.
    """
    if patcher.visit_once(frame_dict):
        for name, value in frame_dict.items():
            if (
                not name.startswith("_")
                and callable(value)
                and id(value) in function_ids
            ):
                patcher.patch(frame_dict, name, _create_wrapped_func(value))

