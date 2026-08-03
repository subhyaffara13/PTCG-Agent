import os

def config_file(kind="local"):
    """Get the filename of the distutils, local, global, or per-user config

    `kind` must be one of "local", "global", or "user"
    """
    if kind == 'local':
        return 'setup.cfg'
    if kind == 'global':
        return os.path.join(os.path.dirname(distutils.__file__), 'distutils.cfg')
    if kind == 'user':
        dot = os.name == 'posix' and '.' or ''
        return os.path.expanduser(convert_path(f"~/{dot}pydistutils.cfg"))
    raise ValueError("config_file() type must be 'local', 'global', or 'user'", kind)

