
def test_ufunc_signatures(ufunc):

    # From _generate_pyx.py
    # "Don't add float32 versions of ufuncs with integer arguments, as this
    # can lead to incorrect dtype selection if the integer arguments are
    # arrays, but float arguments are scalars.
    # This may be a NumPy bug, but we need to work around it.
    # cf. gh-4895, https://github.com/numpy/numpy/issues/5895"
    types = set(sig for sig in ufunc.types
                if not ("l" in sig or "i" in sig or "q" in sig or "p" in sig))

    # Generate the full expanded set of signatures which should exist. There
    # should be matching float and double versions of any existing signature.
    expanded_types = set()
    for sig in types:
        expanded_types.update(
            [sig.replace("d", "f").replace("D", "F"),
             sig.replace("f", "d").replace("F", "D")]
        )
    assert types == expanded_types

