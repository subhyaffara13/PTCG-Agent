
def test_errorbar_uses_rcparams():
    with mpl.rc_context({
        "errorbar.capsize": 5.0,
        "errorbar.capthick": 2.5,
        "errorbar.elinewidth": 1.75,
    }):
        fig, ax = plt.subplots()
        eb = ax.errorbar([0, 1, 2], [1, 2, 3], yerr=[0.1, 0.2, 0.3], fmt="none")

    data_line, caplines, barlinecols = eb.lines
    assert data_line is None
    assert caplines

    assert_allclose([cap.get_markersize() for cap in caplines], 10.0)
    assert_allclose([cap.get_markeredgewidth() for cap in caplines], 2.5)
    for barcol in barlinecols:
        assert_allclose(barcol.get_linewidths(), 1.75)

