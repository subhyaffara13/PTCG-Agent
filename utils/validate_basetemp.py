
def validate_basetemp(path: str) -> str:
    # GH 7119
    msg = "basetemp must not be empty, the current working directory or any parent directory of it"

    # empty path
    if not path:
        raise argparse.ArgumentTypeError(msg)

    def is_ancestor(base: Path, query: Path) -> bool:
        """Return whether query is an ancestor of base."""
        if base == query:
            return True
        return query in base.parents

    # check if path is an ancestor of cwd
    if is_ancestor(Path.cwd(), Path(path).absolute()):
        raise argparse.ArgumentTypeError(msg)

    # check symlinks for ancestors
    if is_ancestor(Path.cwd().resolve(), Path(path).resolve()):
        raise argparse.ArgumentTypeError(msg)

    return path

