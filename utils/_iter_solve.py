
def _iter_solve(a, b, solver=ssl.gcrotmk, **solver_args):
    # work around iterative solvers not accepting multiple r.h.s.

    # also work around a.dtype == float64 and b.dtype == complex128
    # cf https://github.com/scipy/scipy/issues/19644
    if np.issubdtype(b.dtype, np.complexfloating):
        real = _iter_solve(a, b.real, solver, **solver_args)
        imag = _iter_solve(a, b.imag, solver, **solver_args)
        return real + 1j*imag

    if b.ndim == 2 and b.shape[1] !=1:
        res = np.empty_like(b)
        for j in range(b.shape[1]):
            res[:, j], info = solver(a, b[:, j], **solver_args)
            if info != 0:
                raise ValueError(f"{solver = } returns {info =} for column {j}.")
        return res
    else:
        res, info = solver(a, b, **solver_args)
        if info != 0:
            raise ValueError(f"{solver = } returns {info = }.")
        return res

