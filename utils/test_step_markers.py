
def test_step_markers(fig_test, fig_ref):
    fig_test.subplots().step([0, 1], "-o")
    fig_ref.subplots().plot([0, 0, 1], [0, 1, 1], "-o", markevery=[0, 2])

