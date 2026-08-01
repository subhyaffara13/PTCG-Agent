
def to_dtype_bitcast(x: TensorBox, dtype: torch.dtype, *, copy=False):
    x_dtype = x.get_dtype()
    if x_dtype == dtype:
        return clone(x) if copy else x

    def _get_primitive_bitwidth(dtype):
        if dtype.is_floating_point:
            return torch.finfo(dtype).bits
        elif dtype == torch.bool:
            # torch.iinfo doesn't support bool; bools are stored as uint8 (8 bits)
            return 8
        else:
            return torch.iinfo(dtype).bits

    src_bits = _get_primitive_bitwidth(x_dtype)
    dst_bits = _get_primitive_bitwidth(dtype)
    if src_bits != dst_bits:
        # fallback to aten eager implementation for differing bitwidths
        return fallback_handler(aten.view.dtype)(x, dtype)
    else:
        return TensorBox(DtypeView.create(x, dtype))

