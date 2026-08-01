
def test_wrightomega_branch():
    x = -np.logspace(10, 0, 25)
    picut_above = [np.nextafter(np.pi, np.inf)]
    picut_below = [np.nextafter(np.pi, -np.inf)]
    npicut_above = [np.nextafter(-np.pi, np.inf)]
    npicut_below = [np.nextafter(-np.pi, -np.inf)]
    for i in range(50):
        picut_above.append(np.nextafter(picut_above[-1], np.inf))
        picut_below.append(np.nextafter(picut_below[-1], -np.inf))
        npicut_above.append(np.nextafter(npicut_above[-1], np.inf))
        npicut_below.append(np.nextafter(npicut_below[-1], -np.inf))
    y = np.hstack((picut_above, picut_below, npicut_above, npicut_below))
    x, y = np.meshgrid(x, y)
    z = (x + 1j*y).flatten()

    dataset = np.asarray([(z0, complex(_mpmath_wrightomega(z0, 25)))
                          for z0 in z])

    FuncData(sc.wrightomega, dataset, 0, 1, rtol=1e-8).check()

