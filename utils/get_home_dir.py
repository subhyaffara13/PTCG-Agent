
def get_home_dir() -> str:
    """Get the real path of the home directory"""
    homedir = Path("~").expanduser()
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    return str(Path(homedir).resolve())

