
def iterate_exceptions(
    exception: BaseException,
) -> Generator[BaseException, None, None]:
    if isinstance(exception, BaseExceptionGroup):
        for exc in exception.exceptions:
            yield from iterate_exceptions(exc)
    else:
        yield exception

