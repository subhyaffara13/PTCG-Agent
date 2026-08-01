
def test_shichi_consistency():
    # Make sure the implementation of shichi for real arguments agrees
    # with the implementation of shichi for complex arguments.

    # On the negative real axis Cephes drops the imaginary part in chi
    def shichi(x):
        shi, chi = sc.shichi(x + 0j)
        return shi.real, chi.real

    # Overflow happens quickly, so limit range
    x = np.r_[-np.logspace(np.log10(700), -30, 200), 0,
              np.logspace(-30, np.log10(700), 200)]
    shi, chi = sc.shichi(x)
    dataset = np.column_stack((x, shi, chi))
    FuncData(shichi, dataset, 0, (1, 2), rtol=1e-14).check()

