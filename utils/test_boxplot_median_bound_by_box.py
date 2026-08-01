
def test_boxplot_median_bound_by_box(fig_test, fig_ref):
    data = np.arange(3)
    medianprops_test = {"linewidth": 12}
    medianprops_ref = {**medianprops_test, "solid_capstyle": "butt"}
    fig_test.subplots().boxplot(data,  medianprops=medianprops_test)
    fig_ref.subplots().boxplot(data, medianprops=medianprops_ref)

