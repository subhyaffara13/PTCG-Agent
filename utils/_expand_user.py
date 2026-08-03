import os

def _expand_user(filepath_or_buffer: str) -> str: ...


def _expand_user(filepath_or_buffer: BaseBufferT) -> BaseBufferT: ...


def _expand_user(filepath_or_buffer: str | BaseBufferT) -> str | BaseBufferT:
    """
    Return the argument with an initial component of ~ or ~user
    replaced by that user's home directory.

    Parameters
    ----------
    filepath_or_buffer : object to be converted if possible

    Returns
    -------
    expanded_filepath_or_buffer : an expanded filepath or the
                                  input if not expandable
    """
    if isinstance(filepath_or_buffer, str):
        return os.path.expanduser(filepath_or_buffer)
    return filepath_or_buffer

