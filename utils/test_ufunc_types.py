
def test_ufunc_types(ufunc):
    '''
    Check all ufuncs that the correct type is returned. Avoid
    object and boolean types since many operations are not defined for
    for them.

    Choose the shape so even dot and matmul will succeed
    '''
    for typ in ufunc.types:
        # types is a list of strings like ii->i
        if 'O' in typ or '?' in typ:
            continue
        inp, out = typ.split('->')
        if 'm' in inp:
            with pytest.warns(
                DeprecationWarning,
                match="The 'generic' unit for NumPy timedelta is deprecated",
            ):
                args = [np.ones((3, 3), t) for t in inp]
        else:
            args = [np.ones((3, 3), t) for t in inp]
        with warnings.catch_warnings(record=True):
            warnings.filterwarnings("always")
            res = ufunc(*args)
        if isinstance(res, tuple):
            outs = tuple(out)
            assert len(res) == len(outs)
            for r, t in zip(res, outs):
                assert r.dtype == np.dtype(t)
        else:
            assert res.dtype == np.dtype(out)

