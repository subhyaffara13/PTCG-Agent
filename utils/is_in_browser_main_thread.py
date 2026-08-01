
def is_in_browser_main_thread() -> bool:
    return hasattr(js, "window") and hasattr(js, "self") and js.self == js.window


def is_in_browser_main_thread() -> bool:
    return hasattr(js, "window") and hasattr(js, "self") and js.self == js.window

