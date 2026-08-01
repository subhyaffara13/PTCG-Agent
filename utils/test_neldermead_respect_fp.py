
def test_neldermead_respect_fp():
    # Nelder-Mead should respect the fp type of the input + function
    x0 = np.array([5.0, 4.0]).astype(np.float32)
    def rosen_(x):
        assert x.dtype == np.float32
        return optimize.rosen(x)

    optimize.minimize(rosen_, x0, method='Nelder-Mead')

