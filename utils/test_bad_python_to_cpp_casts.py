
def test_bad_python_to_cpp_casts(m):
    with pytest.raises(
        TypeError, match=r"^round_trip_tensor\(\): incompatible function arguments"
    ):
        m.round_trip_tensor(np.zeros((2, 3)))

    with pytest.raises(TypeError, match=r"^Cannot cast array data from dtype"):
        m.round_trip_tensor(np.zeros(dtype=np.str_, shape=(2, 3, 1)))

    with pytest.raises(
        TypeError,
        match=r"^round_trip_tensor_noconvert\(\): incompatible function arguments",
    ):
        m.round_trip_tensor_noconvert(tensor_ref)

    assert_equal_tensor_ref(
        m.round_trip_tensor_noconvert(tensor_ref.astype(np.float64))
    )

    bad_options = "C" if m.needed_options == "F" else "F"
    # Shape, dtype and the order need to be correct for a TensorMap cast
    with pytest.raises(
        TypeError, match=r"^round_trip_view_tensor\(\): incompatible function arguments"
    ):
        m.round_trip_view_tensor(
            np.zeros((3, 5, 2), dtype=np.float64, order=bad_options)
        )

    with pytest.raises(
        TypeError, match=r"^round_trip_view_tensor\(\): incompatible function arguments"
    ):
        m.round_trip_view_tensor(
            np.zeros((3, 5, 2), dtype=np.float32, order=m.needed_options)
        )

    with pytest.raises(
        TypeError, match=r"^round_trip_view_tensor\(\): incompatible function arguments"
    ):
        m.round_trip_view_tensor(
            np.zeros((3, 5), dtype=np.float64, order=m.needed_options)
        )

    temp = np.zeros((3, 5, 2), dtype=np.float64, order=m.needed_options)
    with pytest.raises(
        TypeError, match=r"^round_trip_view_tensor\(\): incompatible function arguments"
    ):
        m.round_trip_view_tensor(
            temp[:, ::-1, :],
        )

    temp = np.zeros((3, 5, 2), dtype=np.float64, order=m.needed_options)
    temp.setflags(write=False)
    with pytest.raises(
        TypeError, match=r"^round_trip_view_tensor\(\): incompatible function arguments"
    ):
        m.round_trip_view_tensor(temp)

