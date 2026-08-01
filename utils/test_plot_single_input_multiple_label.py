
def test_plot_single_input_multiple_label():
    # test ax.plot() with 1D array like input
    # and iterable label
    x = [1, 2, 3]
    y = [2, 5, 6]
    fig, ax = plt.subplots()
    with pytest.raises(ValueError,
                       match='label must be scalar or have the same length'):
        ax.plot(x, y, label=['low', 'high'])

