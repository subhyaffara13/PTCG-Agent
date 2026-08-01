
def test_can_hold_element_bool():
    arr = np.array([], dtype=bool)

    element = True
    assert can_hold_element(arr, element)
    assert can_hold_element(arr, np.array([element]))
    assert can_hold_element(arr, np.array([element], dtype=object))

    element = 1
    assert not can_hold_element(arr, element)
    assert not can_hold_element(arr, np.array([element]))
    assert not can_hold_element(arr, np.array([element], dtype=object))

    element = np.nan
    assert not can_hold_element(arr, element)
    assert not can_hold_element(arr, np.array([element]))
    assert not can_hold_element(arr, np.array([element], dtype=object))

