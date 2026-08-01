
def _format_failed_longrepr(
    item: Item, call: CallInfo[None], excinfo: ExceptionInfo[BaseException]
):
    if call.when == "call":
        longrepr = item.repr_failure(excinfo)
    else:
        # Exception in setup or teardown.
        longrepr = item._repr_failure_py(
            excinfo, style=item.config.getoption("tbstyle", "auto")
        )
    return longrepr

