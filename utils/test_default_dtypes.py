
def test_default_dtypes():
    dtypes = info.default_dtypes()
    assert dtypes["real floating"] == np.float64 == np.asarray(0.0).dtype
    assert dtypes["complex floating"] == np.complex128 == \
        np.asarray(0.0j).dtype
    assert dtypes["integral"] == np.intp == np.asarray(0).dtype
    assert dtypes["indexing"] == np.intp == np.argmax(np.zeros(10)).dtype

    with pytest.raises(ValueError, match="Device not understood"):
        info.default_dtypes(device="gpu")

