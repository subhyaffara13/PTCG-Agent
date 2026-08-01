
def is_final(ann) -> bool:
    return (
        hasattr(ann, "__module__")
        and ann.__module__ in {"typing", "typing_extensions"}
        and (get_origin(ann) is Final or isinstance(ann, type(Final)))
    )

