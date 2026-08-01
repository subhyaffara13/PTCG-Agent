
def test_numpy_dagger():
    if not np:
        skip("numpy not installed.")

    a = np.array([[1.0, 2.0j], [-1.0j, 2.0]])
    adag = a.copy().transpose().conjugate()
    assert (Dagger(a) == adag).all()

