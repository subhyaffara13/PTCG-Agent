
def is_list(ann) -> bool:
    # Check for typing.List missing args (but `list` is fine)
    if ann is typing.List:  # noqa: UP006
        raise_error_container_parameter_missing("List")

    if not hasattr(ann, "__module__"):
        return False

    ann_origin = get_origin(ann)
    return ann.__module__ in ("builtins", "typing") and ann_origin is list


def is_list(obj: object) -> TypeGuard[list[object]]:
    return isinstance(obj, list)

