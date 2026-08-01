
def get_file_mode(fname: str) -> int:
    """Retrieves the file mode corresponding to fname in a filesystem-tolerant manner.

    Parameters
    ----------

    fname : unicode
        The path to the file to get mode from

    """
    # Some filesystems (e.g., CIFS) auto-enable the execute bit on files.  As a result, we
    # should tolerate the execute bit on the file's owner when validating permissions - thus
    # the missing least significant bit on the third octal digit. In addition, we also tolerate
    # the sticky bit being set, so the lsb from the fourth octal digit is also removed.
    return (
        stat.S_IMODE(Path(fname).stat().st_mode) & 0o6677
    )  # Use 4 octal digits since S_IMODE does the same

