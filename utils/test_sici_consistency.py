
def test_sici_consistency():
    # Make sure the implementation of sici for real arguments agrees
    # with the implementation of sici for complex arguments.

    # On the negative real axis Cephes drops the imaginary part in ci
    def sici(x):
        si, ci = sc.sici(x + 0j)
        return si.real, ci.real
    
    x = np.r_[-np.logspace(8, -30, 200), 0, np.logspace(-30, 8, 200)]
    si, ci = sc.sici(x)
    dataset = np.column_stack((x, si, ci))
    FuncData(sici, dataset, 0, (1, 2), rtol=1e-12).check()

