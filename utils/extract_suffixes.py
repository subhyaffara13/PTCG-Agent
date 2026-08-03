import os

def extract_suffixes(iter: Iterable[os.DirEntry[str]], prefix: str) -> Iterator[str]:
    """Return the parts of the paths following the prefix.

    :param iter: Iterator over path names.
    :param prefix: Expected prefix of the path names.
    """
    p_len = len(prefix)
    for entry in iter:
        yield entry.name[p_len:]

