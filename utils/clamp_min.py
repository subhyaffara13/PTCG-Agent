
def clamp_min(
    self: TensorLikeType,
    min: TensorOrNumberLikeType | None = None,
) -> TensorLikeType:
    return torch.clamp(self, min=min)  # type: ignore[arg-type]


def clamp_min(g: jit_utils.GraphContext, self, min):
    min = g.op("Cast", min, to_i=_type_utils.JitScalarType.from_value(self).onnx_type())
    if symbolic_helper._get_tensor_rank(min) == 0:
        max = opset9.unused(g)
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, min, max, opset_before=12
        )
    else:
        return symbolic_helper._op_with_optional_float_cast(
            g, "Max", self, min, opset_before=12
        )


def clamp_min(g: jit_utils.GraphContext, self, min):
    if symbolic_helper._is_constant(min):
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, min_f=symbolic_helper._parse_arg(min, "f"), opset_before=12
        )
    else:
        dtype = _type_utils.JitScalarType.from_value(self)
        min = g.op("Cast", min, to_i=dtype.onnx_type())
        return symbolic_helper._op_with_optional_float_cast(
            g, "Max", self, min, opset_before=12
        )

