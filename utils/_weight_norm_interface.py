
def _weight_norm_interface(v, g, dim=0):
    # https://github.com/pytorch/pytorch/blob/852f8526c52190125446adc9a6ecbcc28fb66182/aten/src/ATen/native/WeightNorm.cpp#L58
    keep_dim = tuple(i for i in range(len(v.shape)) if i != dim)
    # align with cuda behavior, keep norm in 'float' when g is 'bfloat16'
    norm_dtype = torch.float if g.dtype == torch.bfloat16 else None
    norm = v.norm(2, keep_dim, keepdim=True, dtype=norm_dtype)
    return v * (g / norm.to(g.dtype)), norm

