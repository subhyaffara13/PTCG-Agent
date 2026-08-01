
def find_compatible_op_overload(
    op: torch._ops.OpOverloadPacket, args: tuple, kwargs: dict
) -> torch._ops.OpOverload:
    """Find compatible OpOverload for an OpOverloadPacket using provided args and kwargs.

    Each "call_function" fx.Node in the fx.GraphModule has a target that represents a torch._ops.OpOverload.
    The OpOverload contains an OpOverloadPacket that holds all the available overloads for the operation.

    During the type promotion pass, there are cases where the types of the args and kwargs may change,
    such as promoting Python numbers to tensors. Consequently, the original OpOverload might not be
    compatible with the updated args and kwargs. This function is used to identify the compatible
    OpOverload for the given args and kwargs.

    Args:
        op: OpOverloadPacket to find compatible OpOverload for.
        args: The positional arguments to consider for compatibility.
        kwargs: The keyword arguments to consider for compatibility.

    Returns:
        torch._ops.OpOverload: The compatible OpOverload found for the given args and kwargs.

    Raises:
        RuntimeError: If no compatible op overload is found.

    Examples:
        >>> import torch
        >>> packet = torch.ops.aten.pow
        >>> args = (torch.tensor([1.0, 2.0]), 2)
        >>> find_compatible_op_overload(packet, args, {})._overloadname
        'Tensor_Scalar'
        >>> args = (torch.tensor([1.0, 2.0]), torch.tensor(2.0))
        >>> find_compatible_op_overload(packet, args, {})._overloadname
        'Tensor_Tensor'
    """
    # Utilize the dispatch mechanism to find the compatible op overload.
    op_trace_dispatch_mode = _OpTraceDispatchMode()
    with op_trace_dispatch_mode:
        op(*args, **kwargs)
    if len(op_trace_dispatch_mode.traced_ops) < 1:
        raise AssertionError("Expected at least 1 traced op, got 0")

    new_op_overload = op_trace_dispatch_mode.traced_ops[0]
    if not isinstance(new_op_overload, torch._ops.OpOverload):
        raise AssertionError(f"Expected OpOverload, got {type(new_op_overload)}")
    if new_op_overload.overloadpacket != op:
        raise AssertionError(
            f"Expected same OpOverload packet, got {new_op_overload.overloadpacket} != {op}"
        )

    return new_op_overload

