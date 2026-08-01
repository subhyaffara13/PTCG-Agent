
def test_nonzero():
    assert bool(S.Zero) is False
    assert bool(S.One) is True
    assert bool(x) is True
    assert bool(x + y) is True
    assert bool(x - x) is False
    assert bool(x*y) is True
    assert bool(x*1) is True
    assert bool(x*0) is False


def test_nonzero():
    assert ask(Q.nonzero(x)) is None
    assert ask(Q.nonzero(x), Q.real(x)) is None
    assert ask(Q.nonzero(x), Q.positive(x)) is True
    assert ask(Q.nonzero(x), Q.negative(x)) is True
    assert ask(Q.nonzero(x), Q.negative(x) | Q.positive(x)) is True

    assert ask(Q.nonzero(x + y)) is None
    assert ask(Q.nonzero(x + y), Q.positive(x) & Q.positive(y)) is True
    assert ask(Q.nonzero(x + y), Q.positive(x) & Q.negative(y)) is None
    assert ask(Q.nonzero(x + y), Q.negative(x) & Q.negative(y)) is True

    assert ask(Q.nonzero(2*x)) is None
    assert ask(Q.nonzero(2*x), Q.positive(x)) is True
    assert ask(Q.nonzero(2*x), Q.negative(x)) is True
    assert ask(Q.nonzero(x*y), Q.nonzero(x)) is None
    assert ask(Q.nonzero(x*y), Q.nonzero(x) & Q.nonzero(y)) is True

    assert ask(Q.nonzero(x**y), Q.nonzero(x)) is True

    assert ask(Q.nonzero(Abs(x))) is None
    assert ask(Q.nonzero(Abs(x)), Q.nonzero(x)) is True

    assert ask(Q.nonzero(log(exp(2*I)))) is False
    # although this could be False, it is representative of expressions
    # that don't evaluate to a zero with precision
    assert ask(Q.nonzero(cos(1)**2 + sin(1)**2 - 1)) is None


def test_nonzero(dtype):
    # See: gh-28361
    #
    # np.nonzero uses np.count_nonzero to determine the size of the output.
    # array. In a second pass the indices of the non-zero elements are
    # determined, but they can have changed
    #
    # This test triggers a data race which is suppressed in the TSAN CI.
    # The test is to ensure np.nonzero does not generate a segmentation fault
    x = np.random.randint(4, size=100).astype(dtype)
    expected_warning = ('number of non-zero array elements changed'
                        ' during function execution')

    def func(index):
        for _ in range(10):
            if index == 0:
                x[::2] = np.random.randint(2)
            else:
                try:
                    _ = np.nonzero(x)
                except RuntimeError as ex:
                    assert expected_warning in str(ex)

    run_threaded(func, max_workers=10, pass_count=True, outer_iterations=5)


def test_nonzero(strings, na_object):
    dtype = get_dtype(na_object)
    arr = np.array(strings, dtype=dtype)
    is_nonzero = np.array(
        [i for i, item in enumerate(strings) if len(item) != 0])
    assert_array_equal(arr.nonzero()[0], is_nonzero)

    if na_object is not pd_NA and na_object == 'unset':
        return

    strings_with_na = np.array(strings + [na_object], dtype=dtype)
    is_nan = np.isnan(np.array([dtype.na_object], dtype=dtype))[0]

    if is_nan:
        assert strings_with_na.nonzero()[0][-1] == 4
    else:
        assert strings_with_na.nonzero()[0][-1] == 3

    # check that the casting to bool and nonzero give consistent results
    assert_array_equal(strings_with_na[strings_with_na.nonzero()],
                       strings_with_na[strings_with_na.astype(bool)])

