
def test_too_many_figures():
    with pytest.warns(RuntimeWarning):
        for i in range(mpl.rcParams['figure.max_open_warning'] + 1):
            plt.figure()

