import re

def fix_win_path(line: str) -> str:
    r"""Changes Windows paths to Linux paths in error messages.

    E.g. foo\bar.py -> foo/bar.py.
    """
    line = line.replace(root_dir, root_dir.replace("\\", "/"))
    m = re.match(r"^([\S/]+):(\d+:)?(\s+.*)", line)
    if not m:
        return line
    else:
        filename, lineno, message = m.groups()
        return "{}:{}{}".format(filename.replace("\\", "/"), lineno or "", message)

