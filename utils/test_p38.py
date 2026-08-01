
def test_P38():
    M=Matrix([[0, 1, 0],
              [0, 0, 0],
              [0, 0, 0]])

    with raises(AssertionError):
        # raises ValueError: Matrix det == 0; not invertible
        M**S.Half
        # if it doesn't raise then this assertion will be
        # raised and the test will be flagged as not XFAILing
        assert None

