
def test_sequence_length():
    """#2076: Exception raised by len(arg) should be propagated"""

    class BadLen(RuntimeError):
        pass

    class SequenceLike:
        def __getitem__(self, i):
            return None

        def __len__(self):
            raise BadLen()

    with pytest.raises(BadLen):
        m.sequence_length(SequenceLike())

    assert m.sequence_length([1, 2, 3]) == 3
    assert m.sequence_length("hello") == 5

