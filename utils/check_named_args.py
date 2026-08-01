
def check_named_args(distfn, x, shape_args, defaults, meths):
    ## Check calling w/ named arguments.

    # check consistency of shapes, numargs and _parse signature
    signature = _getfullargspec(distfn._parse_args)
    npt.assert_(signature.varargs is None)
    npt.assert_(signature.varkw is None)
    npt.assert_(not signature.kwonlyargs)
    npt.assert_(list(signature.defaults) == list(defaults))

    shape_argnames = signature.args[:-len(defaults)]  # a, b, loc=0, scale=1
    if distfn.shapes:
        shapes_ = distfn.shapes.replace(',', ' ').split()
    else:
        shapes_ = ''
    npt.assert_(len(shapes_) == distfn.numargs)
    npt.assert_(len(shapes_) == len(shape_argnames))

    # check calling w/ named arguments
    shape_args = list(shape_args)

    vals = [meth(x, *shape_args) for meth in meths]
    npt.assert_(np.all(np.isfinite(vals)))

    names, a, k = shape_argnames[:], shape_args[:], {}
    while names:
        k.update({names.pop(): a.pop()})
        v = [meth(x, *a, **k) for meth in meths]
        npt.assert_array_equal(vals, v)
        if 'n' not in k.keys():
            # `n` is first parameter of moment(), so can't be used as named arg
            npt.assert_equal(distfn.moment(1, *a, **k),
                             distfn.moment(1, *shape_args))

    # unknown arguments should not go through:
    k.update({'kaboom': 42})
    assert_raises(TypeError, distfn.cdf, x, **k)

