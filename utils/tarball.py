
def tarball(
    url, target_dir: str | os.PathLike | None = None
) -> Iterator[str | os.PathLike]:
    """
    Get a URL to a tarball, download, extract, yield, then clean up.

    Assumes everything in the tarball is prefixed with a common
    directory. That common path is stripped and the contents
    are extracted to ``target_dir``, similar to passing
    ``-C {target} --strip-components 1`` to the ``tar`` command.

    Uses the streaming protocol to extract the contents from a
    stream in a single pass without loading the whole file into
    memory.

    >>> import urllib.request
    >>> url = getfixture('tarfile_served')
    >>> target = getfixture('tmp_path') / 'out'
    >>> tb = tarball(url, target_dir=target)
    >>> import pathlib
    >>> with tb as extracted:
    ...     contents = pathlib.Path(extracted, 'contents.txt').read_text(encoding='utf-8')
    >>> assert not os.path.exists(extracted)

    If the target is not specified, contents are extracted to a
    directory relative to the current working directory named after
    the name of the file as extracted from the URL.

    >>> target = getfixture('tmp_path')
    >>> with pushd(target), tarball(url):
    ...     target.joinpath('served').is_dir()
    True
    """
    if target_dir is None:
        target_dir = os.path.basename(url).replace('.tar.gz', '').replace('.tgz', '')
    os.mkdir(target_dir)
    try:
        req = urllib.request.urlopen(url)
        with tarfile.open(fileobj=req, mode='r|*') as tf:
            tf.extractall(path=target_dir, filter=_default_filter)
        yield target_dir
    finally:
        shutil.rmtree(target_dir)

