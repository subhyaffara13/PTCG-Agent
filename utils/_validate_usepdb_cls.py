
def _validate_usepdb_cls(value: str) -> tuple[str, str]:
    """Validate syntax of --pdbcls option."""
    try:
        modname, classname = value.split(":")
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"{value!r} is not in the format 'modname:classname'"
        ) from e
    return (modname, classname)

