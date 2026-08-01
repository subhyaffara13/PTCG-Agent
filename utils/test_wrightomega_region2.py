
def test_wrightomega_region2():
    # This region gets less coverage in the TestSystematic test
    x = np.linspace(-2, 1)
    y = np.linspace(-2*np.pi, -1)
    x, y = np.meshgrid(x, y)
    z = (x + 1j*y).flatten()

    dataset = np.asarray([(z0, complex(_mpmath_wrightomega(z0, 25)))
                          for z0 in z])

    FuncData(sc.wrightomega, dataset, 0, 1, rtol=1e-15).check()

