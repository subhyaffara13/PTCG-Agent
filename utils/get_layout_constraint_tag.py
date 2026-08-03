from typing import Any

def get_layout_constraint_tag(
    fn: Any, *, with_default: Literal[True] = True
) -> _C.Tag: ...


def get_layout_constraint_tag(
    fn: Any, *, with_default: Literal[False]
) -> _C.Tag | None: ...


def get_layout_constraint_tag(fn, *, with_default=True):
    for tag in tags_by_priority:
        if tag in fn.tags:
            return tag
    if with_default:
        if is_builtin(fn):
            return _C.Tag.flexible_layout
        import torch._functorch
        from torch._functorch import config

        return getattr(torch._C.Tag, config.custom_op_default_layout_constraint)
    return None

