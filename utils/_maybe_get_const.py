
def _maybe_get_const(
    value: _C.Value | torch.Tensor | Number | Sequence | None,
    descriptor: _ValueDescriptor,
):
    # NOTE: prim::Constant at this stage usually means something not compatible in ONNX,
    # otherwise it'd be converted to onnx::Constant
    # TODO(justinchuby): Replace insinstance with _is_value once we figure out mypy
    if isinstance(value, _C.Value) and _is_onnx_constant(value):
        return _parse_arg(value, descriptor)
    return value

