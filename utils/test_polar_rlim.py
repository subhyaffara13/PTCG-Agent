
def test_polar_rlim(fig_test, fig_ref):
    ax = fig_test.subplots(subplot_kw={'polar': True})
    ax.set_rlim(top=10)
    ax.set_rlim(bottom=.5)

    ax = fig_ref.subplots(subplot_kw={'polar': True})
    ax.set_rmax(10.)
    ax.set_rmin(.5)

