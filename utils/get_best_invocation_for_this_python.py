
def get_best_invocation_for_this_python() -> str:
    """Try to figure out the best way to invoke the current Python."""
    exe = sys.executable
    exe_name = os.path.basename(exe)

    # Try to use the basename, if it's the first executable.
    found_executable = shutil.which(exe_name)
    # Virtual environments often symlink to their parent Python binaries, but we don't
    # want to treat the Python binaries as equivalent when the environment's Python is
    # not on PATH (not activated). Thus, we don't follow symlinks.
    if found_executable and os.path.samestat(os.lstat(found_executable), os.lstat(exe)):
        return exe_name

    # Use the full executable name, because we couldn't find something simpler.
    return exe

