import os

def isfile_strict(path):
    """Same as os.path.isfile() but does not swallow EACCES / EPERM
    exceptions, see:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html.
    """
    try:
        st = os.stat(path)
    except PermissionError:
        raise
    except OSError:
        return False
    else:
        return stat.S_ISREG(st.st_mode)

