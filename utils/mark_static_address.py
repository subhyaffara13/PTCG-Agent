from typing import Any

def mark_static_address(t: Any, guard: bool = False) -> None:
    """
    Marks an input tensor whose address should be treated as constant across calls to the
    same dynamo-compiled function. This indicates to cudagraphs that an extra allocation
    is not needed for this input. The data_ptr will be guarded if guard=True, and cause a full
    recompile if the data_ptr changes. Note: If this address changes, cudagraphs will re-record
    if guard=False.
    """
    if not isinstance(t, torch.Tensor):
        raise TypeError(f"mark_static_address expects a tensor but received {type(t)}")

    if guard:
        t._dynamo_static_input_type = "guarded"  # type: ignore[attr-defined]
    else:
        t._dynamo_static_input_type = "unguarded"  # type: ignore[attr-defined]

