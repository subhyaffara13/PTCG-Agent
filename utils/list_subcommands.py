import sys
from pathlib import Path


def list_subcommands() -> list[str]:
    """List all jupyter subcommands

    searches PATH for `jupyter-name`

    Returns a list of jupyter's subcommand names, without the `jupyter-` prefix.
    Nested children (e.g. jupyter-sub-subsub) are not included.
    """
    subcommand_tuples = set()
    # construct a set of `('foo', 'bar') from `jupyter-foo-bar`
    for d in _path_with_self():
        try:
            bin_paths = list(Path(d).iterdir())
        except OSError:
            continue
        for path in bin_paths:
            name = path.name
            if name.startswith("jupyter-"):
                if sys.platform.startswith("win"):
                    # remove file-extension on Windows
                    name = path.stem
                subcommand_tuples.add(tuple(name.split("-")[1:]))
    # build a set of subcommand strings, excluding subcommands whose parents are defined
    subcommands = set()
    # Only include `jupyter-foo-bar` if `jupyter-foo` is not already present
    for sub_tup in subcommand_tuples:
        if not any(sub_tup[:i] in subcommand_tuples for i in range(1, len(sub_tup))):
            subcommands.add("-".join(sub_tup))
    return sorted(subcommands)

