from typing import Any

def maybe_mark_dynamic(t: Any, index: int | list[Any] | tuple[Any]) -> None:
    """
    Mark a tensor as having a dynamic dim, but don't enforce it (i.e., if this
    dimension ends up getting specialized, don't error).
    """
    if is_traceable_wrapper_subclass(t):
        # default behavior: mirror maybe_mark_dynamic() on all inner tensors with same dim as t
        # TODO: Make this configurable via a supported public API
        _apply_func_to_inner_tensors_of_same_dim(maybe_mark_dynamic, t, index)

    if isinstance(index, int):
        if not hasattr(t, "_dynamo_weak_dynamic_indices"):
            t._dynamo_weak_dynamic_indices = set()
        # TODO(voz): Should we bounds check?

        t._dynamo_weak_dynamic_indices.add(index)
        return

    assert isinstance(index, (list, tuple))
    for i in index:
        maybe_mark_dynamic(t, i)

