
def test_plot_format_kwarg_redundant():
    with pytest.warns(UserWarning, match="marker .* redundantly defined"):
        plt.plot([0], [0], 'o', marker='x')
    with pytest.warns(UserWarning, match="linestyle .* redundantly defined"):
        plt.plot([0], [0], '-', linestyle='--')
    with pytest.warns(UserWarning, match="color .* redundantly defined"):
        plt.plot([0], [0], 'r', color='blue')
    # smoke-test: should not warn
    plt.errorbar([0], [0], fmt='none', color='blue')

