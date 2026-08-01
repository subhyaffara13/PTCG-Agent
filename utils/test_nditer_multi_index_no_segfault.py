
def test_nditer_multi_index_no_segfault():
    class BadSequence:
        def __len__(self):
            return 2

        def __getitem__(self, i):
            if i == 1:
                raise RuntimeError("intentional error")
            return 0

    arr = np.zeros((3, 4))
    it = np.nditer(arr, flags=["multi_index"])
    with pytest.raises(RuntimeError, match="intentional error"):
        it.multi_index = BadSequence()

