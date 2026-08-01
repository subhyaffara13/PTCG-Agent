
def _cossin(x11, x12, x21, x22, separate, swap_sign, compute_u, compute_vh):

    for name, block in zip(["x11", "x12", "x21", "x22"],
                           [x11, x12, x21, x22]):
        if block.shape[1] == 0:
            raise ValueError(f"{name} can't be empty")
    p, q = x11.shape
    mmp, mmq = x22.shape

    if x12.shape != (p, mmq):
        raise ValueError(f"Invalid x12 dimensions: desired {(p, mmq)}, "
                         f"got {x12.shape}")

    if x21.shape != (mmp, q):
        raise ValueError(f"Invalid x21 dimensions: desired {(mmp, q)}, "
                         f"got {x21.shape}")

    if p + mmp != q + mmq:
        raise ValueError("The subblocks have compatible sizes but "
                         "don't form a square array (instead they form a"
                          f" {p + mmp}x{q + mmq} array). This might be "
                          "due to missing p, q arguments.")

    m = p + mmp

    cplx = any([np.iscomplexobj(x) for x in [x11, x12, x21, x22]])
    driver = "uncsd" if cplx else "orcsd"
    csd, csd_lwork = get_lapack_funcs([driver, driver + "_lwork"],
                                      [x11, x12, x21, x22])
    lwork = _compute_lwork(csd_lwork, m=m, p=p, q=q)
    lwork_args = ({'lwork': lwork[0], 'lrwork': lwork[1]} if cplx else
                  {'lwork': lwork})
    *_, theta, u1, u2, v1h, v2h, info = csd(x11=x11, x12=x12, x21=x21, x22=x22,
                                            compute_u1=compute_u,
                                            compute_u2=compute_u,
                                            compute_v1t=compute_vh,
                                            compute_v2t=compute_vh,
                                            trans=False, signs=swap_sign,
                                            **lwork_args)

    method_name = csd.typecode + driver
    if info < 0:
        raise ValueError(f'illegal value in argument {-info} '
                         f'of internal {method_name}')
    if info > 0:
        raise LinAlgError(f"{method_name} did not converge: {info}")

    if separate:
        return (u1, u2), theta, (v1h, v2h)

    U = block_diag(u1, u2)
    VDH = block_diag(v1h, v2h)

    # Construct the middle factor CS
    c = np.diag(np.cos(theta))
    s = np.diag(np.sin(theta))
    r = min(p, q, m - p, m - q)
    n11 = min(p, q) - r
    n12 = min(p, m - q) - r
    n21 = min(m - p, q) - r
    n22 = min(m - p, m - q) - r
    Id = np.eye(np.max([n11, n12, n21, n22, r]), dtype=theta.dtype)
    CS = np.zeros((m, m), dtype=theta.dtype)

    CS[:n11, :n11] = Id[:n11, :n11]

    xs = n11 + r
    xe = n11 + r + n12
    ys = n11 + n21 + n22 + 2 * r
    ye = n11 + n21 + n22 + 2 * r + n12
    CS[xs: xe, ys:ye] = Id[:n12, :n12] if swap_sign else -Id[:n12, :n12]

    xs = p + n22 + r
    xe = p + n22 + r + + n21
    ys = n11 + r
    ye = n11 + r + n21
    CS[xs:xe, ys:ye] = -Id[:n21, :n21] if swap_sign else Id[:n21, :n21]

    CS[p:p + n22, q:q + n22] = Id[:n22, :n22]
    CS[n11:n11 + r, n11:n11 + r] = c
    CS[p + n22:p + n22 + r, n11 + r + n21 + n22:2 * r + n11 + n21 + n22] = c

    xs = n11
    xe = n11 + r
    ys = n11 + n21 + n22 + r
    ye = n11 + n21 + n22 + 2 * r
    CS[xs:xe, ys:ye] = s if swap_sign else -s

    CS[p + n22:p + n22 + r, n11:n11 + r] = -s if swap_sign else s

    return U, CS, VDH

