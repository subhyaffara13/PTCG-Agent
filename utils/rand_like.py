
def rand_like(
    x: torch.Tensor,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=torch.preserve_format,
):
    device = device or x.device
    if device.type != "cuda":
        throw_on_non_cuda(device)
    dtype = dtype or x.dtype
    seed, offset = PhiloxStateTracker.get_state_as_tuple()
    out, offset_jump = torch.ops.rngprims.philox_rand(
        x.shape, seed, offset, None, device, dtype
    )
    PhiloxStateTracker.advance_offset(offset_jump)
    return out


def rand_like(self: torch.Tensor, **kwargs: Any) -> torch.Tensor:
    return _rand_like(torch.rand, self, **kwargs)


def rand_like(
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
        dtype = _type_utils.JitScalarType.from_value(
            self, _type_utils.JitScalarType.FLOAT
        )
    return g.op(
        "RandomUniformLike", self, dtype_i=_type_utils.JitScalarType(dtype).onnx_type()
    )


def rand_like(rng, x):
  shape = np.shape(x)
  dtype = _dtype(x)
  randn = lambda: np.asarray(rng.randn(*shape), dtype=dtype)
  if _dtypes.issubdtype(dtype, np.complexfloating):
    result = randn() + dtype.type(1.0j) * randn()
  else:
    result = randn()
  return result.item() if is_python_scalar(x) else result

