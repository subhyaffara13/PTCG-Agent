
def _get_warning_all_cflag(warning_all: bool = True) -> list[str]:
    if not _IS_WINDOWS:
        return ["Wall"] if warning_all else []
    else:
        return []

