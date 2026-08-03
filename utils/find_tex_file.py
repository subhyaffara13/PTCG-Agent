import os
import sys
from pathlib import Path


def find_tex_file(filename):
    """
    Find a file in the texmf tree using kpathsea_.

    The kpathsea library, provided by most existing TeX distributions, both
    on Unix-like systems and on Windows (MikTeX), is invoked via a long-lived
    luatex process if luatex is installed, or via kpsewhich otherwise.

    .. _kpathsea: https://www.tug.org/kpathsea/

    Parameters
    ----------
    filename : str or path-like

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    """

    # we expect these to always be ascii encoded, but use utf-8
    # out of caution
    if isinstance(filename, bytes):
        filename = filename.decode('utf-8', errors='replace')

    try:
        lk = _LuatexKpsewhich()
    except (FileNotFoundError, OSError):
        lk = None  # Fallback to directly calling kpsewhich, as below.

    if lk:
        path = lk.search(filename)
    else:
        if sys.platform == 'win32':
            # On Windows only, kpathsea can use utf-8 for cmd args and output.
            # The `command_line_encoding` environment variable is set to force
            # it to always use utf-8 encoding.  See Matplotlib issue #11848.
            kwargs = {'env': {**os.environ, 'command_line_encoding': 'utf-8'},
                      'encoding': 'utf-8'}
        else:  # On POSIX, run through the equivalent of os.fsdecode().
            kwargs = {'env': {**os.environ},
                      'encoding': sys.getfilesystemencoding(),
                      'errors': 'surrogateescape'}
        kwargs['env'].update(
            MT_VARTEXFONTS=str(Path(mpl.get_cachedir(), "vartexfonts")))

        try:
            path = cbook._check_and_log_subprocess(
                ['kpsewhich', '-mktex=pk', filename], _log, **kwargs,
            ).rstrip('\n')
        except (FileNotFoundError, OSError, RuntimeError):
            path = None

    if path:
        return path
    else:
        raise FileNotFoundError(
            f"Matplotlib's TeX implementation searched for a file named "
            f"{filename!r} in your texmf tree, but could not find it")

