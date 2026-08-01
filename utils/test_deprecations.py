
def test_deprecations():
    m = Manifold('M', 2)
    p = Patch('P', m)
    with warns_deprecated_sympy():
        CoordSystem('Car2d', p, names=['x', 'y'])

    with warns_deprecated_sympy():
        c = CoordSystem('Car2d', p, ['x', 'y'])

    with warns_deprecated_sympy():
        list(m.patches)

    with warns_deprecated_sympy():
        list(c.transforms)


def test_deprecations(func_name, tcode):
    func = _objs[func_name]

    if tcode in _skip_dict.get(func_name, ''):
        return

    a = np.arange(16).reshape(4, 4) + 8*np.eye(4)
    a = a.T @ a
    a = a.astype(tcode)

    if func_name in _two_arg_names:
        b = a.copy()
        args = (a, b)
    elif func_name in _three_arg_names:
        args = (a, a, a)
    elif func_name in _four_arg_names:
        args = (a, a, a, a)
    elif func_name in _arr_and_int_names:
        args = (a, a.shape[0])
    elif func_name in _arr_and_two_int_names:
        args = (a, a.shape[0], a.shape[1])
    elif func_name in ['cho_solve', 'cho_solve_banded']:
        args = ((a, True), a)
    else:
        args = (a,)

    args = _patch_args(func_name, args)

    with pytest.warns(DeprecationWarning):
        func(*args)


def test_deprecations(name):
    # GH#55139
    msg = f"{name} is deprecated.* Use public APIs instead"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        getattr(internals, name)

