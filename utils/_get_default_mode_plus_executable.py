
def _get_default_mode_plus_executable() -> int:
    return 0o777 & ~current_umask() | 0o111

