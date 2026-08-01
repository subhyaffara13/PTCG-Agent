
def test_violinplot_orientation(fig_test, fig_ref):
    # Test the `orientation : {'vertical', 'horizontal'}`
    # parameter and deprecation of `vert: bool`.
    fig, axs = plt.subplots(nrows=1, ncols=3)
    np.random.seed(19680801)
    all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

    axs[0].violinplot(all_data)  # Default vertical plot.
    # xticks and yticks should be at their default position.
    assert all(axs[0].get_xticks() == np.array(
        [0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5]))
    assert all(axs[0].get_yticks() == np.array(
        [-30., -20., -10., 0., 10., 20., 30.]))

    # Horizontal plot using new `orientation` keyword.
    axs[1].violinplot(all_data, orientation='horizontal')
    # xticks and yticks should be swapped.
    assert all(axs[1].get_xticks() == np.array(
        [-30., -20., -10., 0., 10., 20., 30.]))
    assert all(axs[1].get_yticks() == np.array(
        [0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5]))

    plt.close()

    # Deprecation of `vert: bool` keyword
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match='vert: bool was deprecated in Matplotlib 3.11'):
        # Compare images between a figure that
        # uses vert and one that uses orientation.
        ax_ref = fig_ref.subplots()
        ax_ref.violinplot(all_data, vert=False)

    ax_test = fig_test.subplots()
    ax_test.violinplot(all_data, orientation='horizontal')

