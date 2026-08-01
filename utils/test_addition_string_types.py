
def test_addition_string_types(dt1, dt2):
    arr1 = np.array([1234234], dtype=dt1)
    arr2 = np.array([b"423"], dtype=dt2)
    with pytest.raises(np._core._exceptions.UFuncTypeError) as exc:
        np.add(arr1, arr2)

