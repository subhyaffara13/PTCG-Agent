
def _get_current_locale(lc_var: int = locale.LC_ALL) -> str:
    # getlocale is not always compliant with setlocale, use setlocale. GH#46595
    return locale.setlocale(lc_var)

