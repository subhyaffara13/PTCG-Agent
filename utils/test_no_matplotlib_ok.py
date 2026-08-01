
def test_no_matplotlib_ok():
    msg = (
        'matplotlib is required for plotting when the default backend "matplotlib" is '
        "selected."
    )
    with pytest.raises(ImportError, match=msg):
        pandas.plotting._core._get_plot_backend("matplotlib")

