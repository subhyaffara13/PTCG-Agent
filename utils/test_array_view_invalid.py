
def test_array_view_invalid():
    a = np.ones(100 * 4).astype("uint8")
    with pytest.raises(TypeError):
        m.array_view(a, "deadly_dtype")

