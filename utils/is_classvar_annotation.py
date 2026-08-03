from typing import Any

def is_classvar_annotation(tp: Any, /) -> bool:
    """Return whether the provided argument represents a class variable annotation.

    Although not explicitly stated by the typing specification, `ClassVar` can be used
    inside `Annotated` and as such, this function checks for this specific scenario.

    Because this function is used to detect class variables before evaluating forward references
    (or because evaluation failed), we also implement a naive regex match implementation. This is
    required because class variables are inspected before fields are collected, so we try to be
    as accurate as possible.
    """
    if typing_objects.is_classvar(tp):
        return True

    origin = get_origin(tp)

    if typing_objects.is_classvar(origin):
        return True

    if typing_objects.is_annotated(origin):
        annotated_type = tp.__origin__
        if typing_objects.is_classvar(annotated_type) or typing_objects.is_classvar(get_origin(annotated_type)):
            return True

    str_ann: str | None = None
    if isinstance(tp, typing.ForwardRef):
        str_ann = tp.__forward_arg__
    if isinstance(tp, str):
        str_ann = tp

    if str_ann is not None and _classvar_re.match(str_ann):
        # stdlib dataclasses do something similar, although a bit more advanced
        # (see `dataclass._is_type`).
        return True

    return False

