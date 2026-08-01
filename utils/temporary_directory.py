
def TemporaryDirectory(suffix=None, prefix=None, dir=None, loop=None, executor=None):
    """Async open a temporary directory"""
    return AiofilesContextManagerTempDir(
        _temporary_directory(
            suffix=suffix, prefix=prefix, dir=dir, loop=loop, executor=executor
        )
    )

