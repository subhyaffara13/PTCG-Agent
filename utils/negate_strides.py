
def negate_strides(arrs):
    ret = []
    for a in arrs:
        b = np.zeros_like(a)
        if b.ndim == 2:
            b = b[::-1, ::-1]
        elif b.ndim == 1:
            b = b[::-1]
        else:
            raise ValueError('negate_strides only works for ndim = 1 or'
                             ' 2 arrays')
        b[...] = a
        ret.append(b)
    return ret

