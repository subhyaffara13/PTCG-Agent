
def test_collection_log_datalim(fig_test, fig_ref):
    # Data limits should respect the minimum x/y when using log scale.
    x_vals = [4.38462e-6, 5.54929e-6, 7.02332e-6, 8.88889e-6, 1.12500e-5,
              1.42383e-5, 1.80203e-5, 2.28070e-5, 2.88651e-5, 3.65324e-5,
              4.62363e-5, 5.85178e-5, 7.40616e-5, 9.37342e-5, 1.18632e-4]
    y_vals = [0.0, 0.1, 0.182, 0.332, 0.604, 1.1, 2.0, 3.64, 6.64, 12.1, 22.0,
              39.6, 71.3]

    x, y = np.meshgrid(x_vals, y_vals)
    x = x.flatten()
    y = y.flatten()

    ax_test = fig_test.subplots()
    ax_test.set_xscale('log')
    ax_test.set_yscale('log')
    ax_test.margins = 0
    ax_test.scatter(x, y)

    ax_ref = fig_ref.subplots()
    ax_ref.set_xscale('log')
    ax_ref.set_yscale('log')
    ax_ref.plot(x, y, marker="o", ls="")

