
def test_ravel_axis(install_temp):
    import checks

    assert checks.get_ravel_axis() == np.iinfo("intc").min

