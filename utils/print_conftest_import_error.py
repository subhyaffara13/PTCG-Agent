
def print_conftest_import_error(e: ConftestImportFailure, file: TextIO) -> None:
    exc_info = ExceptionInfo.from_exception(e.cause)
    tw = TerminalWriter(file)
    tw.line(f"ImportError while loading conftest '{e.path}'.", red=True)
    exc_info.traceback = exc_info.traceback.filter(
        filter_traceback_for_conftest_import_failure
    )
    exc_repr = (
        exc_info.getrepr(style="short", chain=False)
        if exc_info.traceback
        else exc_info.exconly()
    )
    formatted_tb = str(exc_repr)
    for line in formatted_tb.splitlines():
        tw.line(line.rstrip(), red=True)

