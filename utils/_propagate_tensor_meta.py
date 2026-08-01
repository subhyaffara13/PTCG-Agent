
def _propagate_tensor_meta(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> TensorMeta:
    op_info = DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)
    if op_info.schema is None:
        raise AssertionError(
            "op_info.schema should not be None after unwrap_to_op_info"
        )
    tensor_meta = DTensor._op_dispatcher.sharding_propagator._propagate_tensor_meta(
        op_info.schema
    )
    if isinstance(tensor_meta, TensorMeta):
        return tensor_meta
    elif isinstance(tensor_meta, tuple):
        # pyrefly: ignore [bad-return]
        return tensor_meta[0]
    else:
        raise RuntimeError(f"Unexpected tensor meta type: {type(tensor_meta)}.")

