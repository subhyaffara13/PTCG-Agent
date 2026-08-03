import os

def _format_exception_group_all_skipped_longrepr(
    item: Item,
    excinfo: ExceptionInfo[BaseExceptionGroup[BaseException | BaseExceptionGroup]],
) -> tuple[str, int, str]:
    r = excinfo._getreprcrash()
    assert r is not None, (
        "There should always be a traceback entry for skipping a test."
    )
    if all(
        getattr(skip, "_use_item_location", False) for skip in excinfo.value.exceptions
    ):
        path, line = item.reportinfo()[:2]
        assert line is not None
        loc = (os.fspath(path), line + 1)
        default_msg = "skipped"
    else:
        loc = (str(r.path), r.lineno)
        default_msg = r.message

    # Get all unique skip messages.
    msgs: list[str] = []
    for exception in excinfo.value.exceptions:
        m = getattr(exception, "msg", None) or (
            exception.args[0] if exception.args else None
        )
        if m and m not in msgs:
            msgs.append(m)

    reason = "; ".join(msgs) if msgs else default_msg
    longrepr = (*loc, reason)
    return longrepr

