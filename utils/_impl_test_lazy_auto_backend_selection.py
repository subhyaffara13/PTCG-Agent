
def _impl_test_lazy_auto_backend_selection():
    import matplotlib
    import matplotlib.pyplot as plt
    # just importing pyplot should not be enough to trigger resolution
    bk = matplotlib.rcParams._get('backend')
    assert not isinstance(bk, str)
    assert plt._backend_mod is None
    # but actually plotting should
    plt.plot(5)
    assert plt._backend_mod is not None
    bk = matplotlib.rcParams._get('backend')
    assert isinstance(bk, str)

