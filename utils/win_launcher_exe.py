
def win_launcher_exe(prefix):
    """A simple routine to select launcher script based on platform."""
    assert prefix in ('cli', 'gui')
    if platform.machine() == "ARM64":
        return f"{prefix}-arm64.exe"
    else:
        return f"{prefix}-32.exe"

