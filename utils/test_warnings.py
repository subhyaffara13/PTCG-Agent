
def test_warnings():
    # ticket 1334
    with np.errstate(all='raise'):
        # these should raise no fp warnings
        _ufuncs.eval_legendre(1, 0)
        _ufuncs.eval_laguerre(1, 1)
        _ufuncs.eval_gegenbauer(1, 1, 0)


def test_warnings():
    # This test is an echo of the previous behavior, which was to raise a
    # warning if the user triggered a search for mat files on the Python system
    # path. We can remove the test in the next version after upcoming (0.13).
    fname = pjoin(test_data_path, 'testdouble_7.1_GLNX86.mat')
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        # This should not generate a warning
        loadmat(fname, struct_as_record=True)
        # This neither
        loadmat(fname, struct_as_record=False)

