
def _nbool_correspond_all(u, v, w=None):
    if u.dtype == v.dtype == bool and w is None:
        not_u = ~u
        not_v = ~v
        nff = (not_u & not_v).sum()
        nft = (not_u & v).sum()
        ntf = (u & not_v).sum()
        ntt = (u & v).sum()
    else:
        dtype = np.result_type(int, u.dtype, v.dtype)
        u = u.astype(dtype)
        v = v.astype(dtype)
        not_u = 1.0 - u
        not_v = 1.0 - v
        if w is not None:
            not_u = w * not_u
            u = w * u
        nff = (not_u * not_v).sum()
        nft = (not_u * v).sum()
        ntf = (u * not_v).sum()
        ntt = (u * v).sum()
    return (nff, nft, ntf, ntt)

