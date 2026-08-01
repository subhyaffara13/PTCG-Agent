
def register_plotting_backend_cb(key: str | None) -> None:
    if key == "matplotlib":
        # We defer matplotlib validation, since it's the default
        return
    from pandas.plotting._core import _get_plot_backend

    _get_plot_backend(key)

