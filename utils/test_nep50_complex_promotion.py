
def test_nep50_complex_promotion():
    with pytest.warns(RuntimeWarning, match=".*overflow"):
        res = np.complex64(3) + complex(2**300)

    assert type(res) is np.complex64

