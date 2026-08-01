
def get_win_launcher(type):
    """
    Load the Windows launcher (executable) suitable for launching a script.

    `type` should be either 'cli' or 'gui'

    Returns the executable as a byte string.
    """
    launcher_fn = f'{type}.exe'
    if is_64bit():
        if get_platform() == "win-arm64":
            launcher_fn = launcher_fn.replace(".", "-arm64.")
        else:
            launcher_fn = launcher_fn.replace(".", "-64.")
    else:
        launcher_fn = launcher_fn.replace(".", "-32.")
    return resources.files('setuptools').joinpath(launcher_fn).read_bytes()

