
def _assert_equal_on_sequences(actual, desired, err_msg=''):
    """
    Asserts the equality of two non-array sequences.

    """
    assert_equal(len(actual), len(desired), err_msg)
    for k in range(len(desired)):
        assert_equal(actual[k], desired[k], f'item={k!r}\n{err_msg}')

