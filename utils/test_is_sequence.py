
def test_is_sequence():
    is_seq = inference.is_sequence
    assert is_seq((1, 2))
    assert is_seq([1, 2])
    assert not is_seq("abcd")
    assert not is_seq(np.int64)

    class A:
        def __getitem__(self, item):
            return 1

    assert not is_seq(A())

