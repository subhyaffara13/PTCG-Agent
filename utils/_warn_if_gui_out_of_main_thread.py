
def _warn_if_gui_out_of_main_thread() -> None:
    warn = False
    canvas_class = cast(type[FigureCanvasBase], _get_backend_mod().FigureCanvas)
    if canvas_class.required_interactive_framework:
        if hasattr(threading, 'get_native_id'):
            # This compares native thread ids because even if Python-level
            # Thread objects match, the underlying OS thread (which is what
            # really matters) may be different on Python implementations with
            # green threads.
            if threading.get_native_id() != threading.main_thread().native_id:
                warn = True
        else:
            # Fall back to Python-level Thread if native IDs are unavailable,
            # mainly for PyPy.
            if threading.current_thread() is not threading.main_thread():
                warn = True
    if warn:
        _api.warn_external(
            "Starting a Matplotlib GUI outside of the main thread will likely "
            "fail.")

