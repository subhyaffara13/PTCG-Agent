
def test_bounds_check(arr):
    for func in (
        m.index_at,
        m.index_at_t,
        m.data,
        m.data_t,
        m.mutate_data,
        m.mutate_data_t,
        m.at_t,
        m.mutate_at_t,
    ):
        with pytest.raises(IndexError) as excinfo:
            func(arr, 2, 0)
        assert str(excinfo.value) == "index 2 is out of bounds for axis 0 with size 2"
        with pytest.raises(IndexError) as excinfo:
            func(arr, 0, 4)
        assert str(excinfo.value) == "index 4 is out of bounds for axis 1 with size 3"


def test_bounds_check():
    # GH21796
    with pytest.raises(
        TypeError, match=r"cannot safely cast non-equivalent int(32|64) to uint16"
    ):
        pd.array([-1, 2, 3], dtype="UInt16")

