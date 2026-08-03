from typing import Callable

def thread_exception_hook(
    args: threading.ExceptHookArgs,
    /,
    *,
    append: Callable[[ThreadExceptionMeta | BaseException], object],
) -> None:
    try:
        # we need to compute these strings here as they might change after
        # the excepthook finishes and before the metadata object is
        # collected by a pytest hook
        thread_name = "<unknown>" if args.thread is None else args.thread.name
        summary = f"Exception in thread {thread_name}"
        traceback_message = "\n\n" + "".join(
            traceback.format_exception(
                args.exc_type,
                args.exc_value,
                args.exc_traceback,
            )
        )
        tracemalloc_tb = "\n" + tracemalloc_message(args.thread)
        msg = summary + traceback_message + tracemalloc_tb
        cause_msg = summary + tracemalloc_tb

        append(
            ThreadExceptionMeta(
                # Compute these strings here as they might change later
                msg=msg,
                cause_msg=cause_msg,
                exc_value=args.exc_value,
            )
        )
    except BaseException as e:
        append(e)
        # Raising this will cause the exception to be logged twice, once in our
        # collect_thread_exception and once by sys.excepthook
        # which is fine - this should never happen anyway and if it does
        # it should probably be reported as a pytest bug.
        raise

