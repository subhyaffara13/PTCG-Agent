
def clamp_max(
    self: TensorLikeType,
    max: TensorOrNumberLikeType | None = None,
) -> TensorLikeType:
    return torch.clamp(self, max=max)  # type: ignore[arg-type]


def clamp_max(g: jit_utils.GraphContext, self, max):
    max = g.op("Cast", max, to_i=_type_utils.JitScalarType.from_value(self).onnx_type())
    if symbolic_helper._get_tensor_rank(max) == 0:
        min = opset9.unused(g)
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, min, max, opset_before=12
        )
    else:
        return symbolic_helper._op_with_optional_float_cast(
            g, "Min", self, max, opset_before=12
        )


def clamp_max(g: jit_utils.GraphContext, self, max):
    if symbolic_helper._is_constant(max):
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, max_f=symbolic_helper._parse_arg(max, "f"), opset_before=12
        )
    else:
        dtype = _type_utils.JitScalarType.from_value(self)
        max = g.op("Cast", max, to_i=dtype.onnx_type())
        return symbolic_helper._op_with_optional_float_cast(
            g, "Min", self, max, opset_before=12
        )

