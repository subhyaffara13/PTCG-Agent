import os
import re
import sys

def matches_exclude(
    subpath: str, excludes: list[str], fscache: FileSystemCache, verbose: bool
) -> bool:
    if not excludes:
        return False
    subpath_str = os.path.relpath(subpath).replace(os.sep, "/")
    if fscache.isdir(subpath):
        subpath_str += "/"
    for exclude in excludes:
        try:
            if re.search(exclude, subpath_str):
                if verbose:
                    print(
                        f"TRACE: Excluding {subpath_str} (matches pattern {exclude})",
                        file=sys.stderr,
                    )
                return True
        except re.error as e:
            print(
                f"error: The exclude {exclude} is an invalid regular expression, because: {e}"
                + (
                    "\n(Hint: use / as a path separator, even if you're on Windows!)"
                    if "\\" in exclude
                    else ""
                )
                + "\nFor more information on Python's flavor of regex, see:"
                + " https://docs.python.org/3/library/re.html",
                file=sys.stderr,
            )
            sys.exit(2)
    return False

