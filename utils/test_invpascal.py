
def test_invpascal():

    def check_invpascal(n, kind, exact):
        ip = invpascal(n, kind=kind, exact=exact)
        p = pascal(n, kind=kind, exact=exact)
        # Matrix-multiply ip and p, and check that we get the identity matrix.
        # We can't use the simple expression e = ip.dot(p), because when
        # n < 35 and exact is True, p.dtype is np.uint64 and ip.dtype is
        # np.int64. The product of those dtypes is np.float64, which loses
        # precision when n is greater than 18.  Instead we'll cast both to
        # object arrays, and then multiply.
        e = ip.astype(object).dot(p.astype(object))
        assert_array_equal(e, eye(n), err_msg=f"n={n}  kind={kind!r} exact={exact!r}")

    kinds = ['symmetric', 'lower', 'upper']

    ns = [1, 2, 5, 18]
    for n in ns:
        for kind in kinds:
            for exact in [True, False]:
                check_invpascal(n, kind, exact)

    ns = [19, 34, 35, 50]
    for n in ns:
        for kind in kinds:
            check_invpascal(n, kind, True)

