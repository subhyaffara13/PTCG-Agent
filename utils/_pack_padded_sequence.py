
def _pack_padded_sequence(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    inputs: FakeTensor,
    lengths: FakeTensor,
    batch_first: bool,
) -> tuple[FakeTensor, FakeTensor]:
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    new_batch_size = fake_mode.shape_env.create_unbacked_symint()

    from torch.fx.experimental.symbolic_shapes import _constrain_range_for_size

    _constrain_range_for_size(new_batch_size)

    if not batch_first:
        # Inputs should have shape (batch_size, seq_len, *)
        inputs = inputs.transpose(0, 1)  # type: ignore[assignment]

    res_size = inputs.shape[1:]
    packed_data = inputs.new_empty(res_size)
    batch_size = inputs.new_empty((new_batch_size,))
    return (packed_data, batch_size)  # type: ignore[return]


def _pack_padded_sequence(g: jit_utils.GraphContext, input, lengths, batch_first):
    # Currently there is no PackPadded operator in ONNX. We rely on an
    # optimization pass to remove this later. It is an error if all
    # PackPadded operators cannot be optimized out.
    if batch_first:
        input = g.op("Transpose", input, perm_i=[1, 0, 2])
    if not lengths.type().isSubtypeOf(torch._C.TensorType.get()):
        raise errors.SymbolicValueError(
            "'lengths' must be a Tensor for ONNX export", input
        )
    # We know it's a TensorType so this check is now safe.
    # It's really only necessary because those operators expand to something that
    # only works with int32 types in Caffe2...
    if (
        _type_utils.JitScalarType.from_value(
            lengths, _type_utils.JitScalarType.UNDEFINED
        )
        != _type_utils.JitScalarType.INT
    ):
        lengths = g.op("Cast", lengths, to_i=_C_onnx.TensorProtoDataType.INT32)
    return g.op("prim::PackPadded", input, lengths, outputs=2)

