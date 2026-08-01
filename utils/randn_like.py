
def randn_like(self: torch.Tensor, **kwargs: Any) -> torch.Tensor:
    return _rand_like(torch.randn, self, **kwargs)


def randn_like(
    g: jit_utils.GraphContext,
    self,
    dtype,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.from_value(
            self, _type_utils.JitScalarType.FLOAT
        )
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    return g.op("RandomNormalLike", self, dtype_i=scalar_type.onnx_type())

