
def test_wrightomega_real_versus_complex():
    x = np.linspace(-500, 500, 1001)
    results = sc.wrightomega(x + 0j).real
    assert_func_equal(sc.wrightomega, results, x, atol=0, rtol=1e-14)

