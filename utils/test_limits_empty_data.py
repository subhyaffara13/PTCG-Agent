
def test_limits_empty_data(plot_fun, fig_test, fig_ref):
    # Check that plotting empty data doesn't change autoscaling of dates
    x = np.arange("2010-01-01", "2011-01-01", dtype="datetime64[D]")

    ax_test = fig_test.subplots()
    ax_ref = fig_ref.subplots()

    getattr(ax_test, plot_fun)([], [])

    for ax in [ax_test, ax_ref]:
        getattr(ax, plot_fun)(x, range(len(x)), color='C0')

