
def new_figure_manager(*args, **kwargs):
    """Create a new figure manager instance."""
    _warn_if_gui_out_of_main_thread()
    return _get_backend_mod().new_figure_manager(*args, **kwargs)

