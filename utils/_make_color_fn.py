
def _make_color_fn(code):
    def f(s):
        reset = "\033[0m"
        return f"{code}{s}{reset}"

    return f

