
def test_figure_hook():

    test_rc = {
        'figure.hooks': ['matplotlib.tests.test_pyplot:figure_hook_example']
    }
    with mpl.rc_context(test_rc):
        fig = plt.figure()

    assert fig._test_was_here

