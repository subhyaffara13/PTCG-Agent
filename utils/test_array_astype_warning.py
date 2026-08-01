
def test_array_astype_warning(t):
    # test ComplexWarning when casting from complex to float or int
    a = np.array(10, dtype=np.complex128)
    pytest.warns(np.exceptions.ComplexWarning, a.astype, t)

