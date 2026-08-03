import re

def parse_cwd(line: str) -> str | None:
    """Parse the second line of the program for the command line.

    This should have the form

      # cwd: <directory>

    For example:

      # cwd: main/subdir
    """
    m = re.match("# cwd: (.*)$", line)
    return m.group(1) if m else None

