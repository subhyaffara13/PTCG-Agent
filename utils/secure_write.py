import os
from typing import Any
from pathlib import Path


def secure_write(fname: str, binary: bool = False) -> Iterator[Any]:
    """Opens a file in the most restricted pattern available for
    writing content. This limits the file mode to `0o0600` and yields
    the resulting opened filed handle.

    Parameters
    ----------

    fname : unicode
        The path to the file to write

    binary: boolean
        Indicates that the file is binary
    """
    mode = "wb" if binary else "w"
    encoding = None if binary else "utf-8"
    open_flag = os.O_CREAT | os.O_WRONLY | os.O_TRUNC
    try:
        Path(fname).unlink()
    except OSError:
        # Skip any issues with the file not existing
        pass

    if os.name == "nt":
        if allow_insecure_writes:
            # Mounted file systems can have a number of failure modes inside this block.
            # For windows machines in insecure mode we simply skip this to avoid failures :/
            issue_insecure_write_warning()
        else:
            # Python on windows does not respect the group and public bits for chmod, so we need
            # to take additional steps to secure the contents.
            # Touch file preemptively to avoid editing permissions in open files in Windows
            fd = os.open(fname, open_flag, 0o0600)
            os.close(fd)
            open_flag = os.O_WRONLY | os.O_TRUNC
            win32_restrict_file_to_user(fname)

    with os.fdopen(os.open(fname, open_flag, 0o0600), mode, encoding=encoding) as f:
        if os.name != "nt":
            # Enforce that the file got the requested permissions before writing
            file_mode = get_file_mode(fname)
            if file_mode != 0o0600:
                if allow_insecure_writes:
                    issue_insecure_write_warning()
                else:
                    msg = (
                        f"Permissions assignment failed for secure file: '{fname}'."
                        f" Got '{oct(file_mode)}' instead of '0o0600'."
                    )
                    raise RuntimeError(msg)
        yield f

