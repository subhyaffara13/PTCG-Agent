
def _rough_check(a, b, compare_assert=assert_allclose_forgiving,
                  key=lambda x: x, w=None):
    check_a = key(a)
    check_b = key(b)
    try:
        if np.array(check_a != check_b).any():  # try strict equality for string types
            compare_assert(check_a, check_b)
    except AttributeError:  # masked array
        compare_assert(check_a, check_b)
    except (TypeError, ValueError):  # nested data structure
        for a_i, b_i in zip(check_a, check_b):
            _rough_check(a_i, b_i, compare_assert=compare_assert)

