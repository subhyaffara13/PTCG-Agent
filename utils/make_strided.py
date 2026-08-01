
def make_strided(arrs):
    strides = [(3, 7), (2, 2), (3, 4), (4, 2), (5, 4), (2, 3), (2, 1), (4, 5)]
    kmax = len(strides)
    k = 0
    ret = []
    for a in arrs:
        if a.ndim == 1:
            s = strides[k % kmax]
            k += 1
            base = np.zeros(s[0]*a.shape[0]+s[1], a.dtype)
            view = base[s[1]::s[0]]
            view[...] = a
        elif a.ndim == 2:
            s = strides[k % kmax]
            t = strides[(k+1) % kmax]
            k += 2
            base = np.zeros((s[0]*a.shape[0]+s[1], t[0]*a.shape[1]+t[1]),
                            a.dtype)
            view = base[s[1]::s[0], t[1]::t[0]]
            view[...] = a
        else:
            raise ValueError('make_strided only works for ndim = 1 or'
                             ' 2 arrays')
        ret.append(view)
    return ret

