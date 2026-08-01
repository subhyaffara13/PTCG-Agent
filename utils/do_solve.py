
def do_solve(**kw):
    if not hasattr(niter, 'n'):
        niter.n = [0]

    if not hasattr(count, 'c'):
        count.c = [0]

    count.c[0] = 0
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", ".*called without specifying.*", DeprecationWarning)
        x0, flag = gcrotmk(A, b, x0=zeros(A.shape[0]), rtol=1e-14, **kw)
    count_0 = count.c[0]
    assert_(allclose(A@x0, b, rtol=1e-12, atol=1e-12), norm(A@x0-b))
    return x0, count_0


def do_solve(**kw):
    if not hasattr(niter, 'n'):
        niter.n = [0]
    if not hasattr(count, 'c'):
        count.c = [0]
    count.c[0] = 0
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", ".*called without specifying.*", DeprecationWarning)
        x0, flag = lgmres(A, b, x0=zeros(A.shape[0]),
                          inner_m=6, rtol=1e-14, **kw)
    count_0 = count.c[0]
    assert_(allclose(A@x0, b, rtol=1e-12, atol=1e-12), norm(A@x0-b))
    return x0, count_0

