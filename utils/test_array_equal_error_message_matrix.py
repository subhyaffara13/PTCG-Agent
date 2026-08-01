
def test_array_equal_error_message_matrix():
    # 2018-04-29: moved here from testing.tests.test_utils.
    with pytest.raises(AssertionError) as exc_info:
        assert_equal(np.array([1, 2]), np.matrix([1, 2]))
    msg = str(exc_info.value)
    msg_reference = textwrap.dedent("""\

    Arrays are not equal

    (shapes (2,), (1, 2) mismatch)
     ACTUAL: array([1, 2])
     DESIRED: matrix([[1, 2]])""")
    assert_equal(msg, msg_reference)

