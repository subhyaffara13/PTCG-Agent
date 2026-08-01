
def upgrade_pip(python_executable: str) -> None:
    """Install pip>=21.3.1. Required for editable installs with PEP 660."""
    if sys.version_info >= (3, 11) or (3, 10, 3) <= sys.version_info < (3, 11):
        # Skip for more recent Python releases which come with pip>=21.3.1
        # out of the box - for performance reasons.
        return

    install_cmd = [python_executable, "-m", "pip", "install", "pip>=21.3.1"]
    try:
        with filelock.FileLock(pip_lock, timeout=pip_timeout):
            proc = subprocess.run(install_cmd, capture_output=True, env=os.environ)
    except filelock.Timeout as err:
        raise Exception(f"Failed to acquire {pip_lock}") from err
    if proc.returncode != 0:
        raise Exception(proc.stdout.decode("utf-8") + proc.stderr.decode("utf-8"))

