
def select_one(x, mask, dim, keep_dims=False):
    idtype = tl.core.get_int_dtype(x.dtype.primitive_bitwidth, signed=False)
    ix = x.to(idtype, bitcast=True)
    iy = tl.sum(ix * mask, dim, keep_dims=keep_dims)
    return iy.to(idtype).to(x.dtype, bitcast=True)

