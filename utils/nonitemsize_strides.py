
def nonitemsize_strides(arrs):
    out = []
    for a in arrs:
        a_dtype = a.dtype
        b = np.zeros(a.shape, [('a', a_dtype), ('junk', 'S1')])
        c = b.getfield(a_dtype)
        c[...] = a
        out.append(c)
    return out

