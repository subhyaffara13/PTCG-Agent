
def TemporaryFile(
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
    """Async open an unnamed temporary file"""
    return AiofilesContextManager(
        _temporary_file(
            named=False,
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

