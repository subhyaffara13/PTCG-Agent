
def _encode_pth(content: str) -> bytes:
    """
    Prior to Python 3.13 (see https://github.com/python/cpython/issues/77102),
    .pth files are always read with 'locale' encoding, the recommendation
    from the cpython core developers is to write them as ``open(path, "w")``
    and ignore warnings (see python/cpython#77102, pypa/setuptools#3937).
    This function tries to simulate this behavior without having to create an
    actual file, in a way that supports a range of active Python versions.
    (There seems to be some variety in the way different version of Python handle
    ``encoding=None``, not all of them use ``locale.getpreferredencoding(False)``
    or ``locale.getencoding()``).
    """
    with io.BytesIO() as buffer:
        wrapper = io.TextIOWrapper(buffer, encoding=py312.PTH_ENCODING)
        # TODO: Python 3.13 replace the whole function with `bytes(content, "utf-8")`
        wrapper.write(content)
        wrapper.flush()
        buffer.seek(0)
        return buffer.read()

