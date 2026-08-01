
def test_polar_log_rorigin(fig_ref, fig_test):
    # Test that equivalent linear and log radial settings give the same axes patch
    # and spines.
    ax_ref = fig_ref.add_subplot(projection='polar', facecolor='red')
    ax_ref.set_rlim(0, 2)
    ax_ref.set_rorigin(-3)
    ax_ref.set_rticks(np.linspace(0, 2, 5))

    ax_test = fig_test.add_subplot(projection='polar', facecolor='red')
    ax_test.set_rscale('log')
    ax_test.set_rlim(1, 100)
    ax_test.set_rorigin(10**-3)
    ax_test.set_rticks(np.logspace(0, 2, 5))

    for ax in ax_ref, ax_test:
        # Radial tick labels should be the only difference, so turn them off.
        ax.tick_params(labelleft=False)

