
def test_can_hold_element_categorical():
    # GH#56376
    arr = np.array([], dtype=np.float64)
    cat = Categorical([1, 2, None])

    assert can_hold_element(arr, cat)

