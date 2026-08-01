
def unraisable_hook(
    unraisable: sys.UnraisableHookArgs,
    /,
    *,
    append: Callable[[UnraisableMeta | BaseException], object],
) -> None:
    try:
        # we need to compute these strings here as they might change after
        # the unraisablehook finishes and before the metadata object is
        # collected by a pytest hook
        err_msg = (
            "Exception ignored in" if unraisable.err_msg is None else unraisable.err_msg
        )
        summary = f"{err_msg}: {unraisable.object!r}"
        traceback_message = "\n\n" + "".join(
            traceback.format_exception(
                unraisable.exc_type,
                unraisable.exc_value,
                unraisable.exc_traceback,
            )
        )
        tracemalloc_tb = "\n" + tracemalloc_message(unraisable.object)
        msg = summary + traceback_message + tracemalloc_tb
        cause_msg = summary + tracemalloc_tb

        append(
            UnraisableMeta(
                msg=msg,
                cause_msg=cause_msg,
                exc_value=unraisable.exc_value,
            )
        )
    except BaseException as e:
        append(e)
        # Raising this will cause the exception to be logged twice, once in our
        # collect_unraisable and once by the unraisablehook calling machinery
        # which is fine - this should never happen anyway and if it does
        # it should probably be reported as a pytest bug.
        raise

