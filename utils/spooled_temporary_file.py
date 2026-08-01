
def SpooledTemporaryFile(
    max_size=0,
    mode="w+b",
    buffering=-1,
    encoding=None,
    newline=None,
    suffix=None,
    prefix=None,
    dir=None,
    loop=None,
    executor=None,
):
    """Async open a spooled temporary file"""
    return AiofilesContextManager(
        _spooled_temporary_file(
            max_size=max_size,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            newline=newline,
            suffix=suffix,
            prefix=prefix,
            dir=dir,
            loop=loop,
            executor=executor,
        )
    )

