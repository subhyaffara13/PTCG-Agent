
def test_boxplot_orientation(fig_test, fig_ref):
    # Test the `orientation : {'vertical', 'horizontal'}`
    # parameter and deprecation of `vert: bool`.
    fig, axs = plt.subplots(nrows=1, ncols=2)
    np.random.seed(19680801)
    all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

    axs[0].boxplot(all_data)  # Default vertical plot.
    # xticks and yticks should be at their default position.
    assert all(axs[0].get_xticks() == np.array(
        [1, 2, 3, 4]))
    assert all(axs[0].get_yticks() == np.array(
        [-30., -20., -10., 0., 10., 20., 30.]))

    # Horizontal plot using new `orientation` keyword.
    axs[1].boxplot(all_data, orientation='horizontal')
    # xticks and yticks should be swapped.
    assert all(axs[1].get_xticks() == np.array(
        [-30., -20., -10., 0., 10., 20., 30.]))
    assert all(axs[1].get_yticks() == np.array(
        [1, 2, 3, 4]))

    plt.close()

    # Deprecation of `vert: bool` keyword and
    # 'boxplot.vertical' rcparam.
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='was deprecated in Matplotlib 3.10'):
        # Compare images between a figure that
        # uses vert and one that uses orientation.
        with mpl.rc_context({'boxplot.vertical': False}):
            ax_ref = fig_ref.subplots()
            ax_ref.boxplot(all_data)

        ax_test = fig_test.subplots()
        ax_test.boxplot(all_data, orientation='horizontal')

