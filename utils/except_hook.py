import os
import sys

def except_hook(
    exc_type: type[BaseException], exc_value: BaseException, tb: TracebackType | None
) -> None:
    exception_config: DeveloperExceptionConfig | None = getattr(
        exc_value, _typer_developer_exception_attr_name, None
    )
    standard_traceback = os.getenv(
        "TYPER_STANDARD_TRACEBACK", os.getenv("_TYPER_STANDARD_TRACEBACK")
    )
    if (
        standard_traceback
        or not exception_config
        or not exception_config.pretty_exceptions_enable
    ):
        _original_except_hook(exc_type, exc_value, tb)
        return
    typer_path = os.path.dirname(__file__)
    click_path = os.path.dirname(click.__file__)
    internal_dir_names = [typer_path, click_path]
    exc = exc_value
    if HAS_RICH:
        from . import rich_utils

        rich_tb = rich_utils.get_traceback(exc, exception_config, internal_dir_names)
        console_stderr = rich_utils._get_rich_console(stderr=True)
        console_stderr.print(rich_tb)
        return
    tb_exc = traceback.TracebackException.from_exception(exc)
    stack: list[FrameSummary] = []
    for frame in tb_exc.stack:
        if any(frame.filename.startswith(path) for path in internal_dir_names):
            if not exception_config.pretty_exceptions_short:
                # Hide the line for internal libraries, Typer and Click
                stack.append(
                    traceback.FrameSummary(
                        filename=frame.filename,
                        lineno=frame.lineno,
                        name=frame.name,
                        line="",
                    )
                )
        else:
            stack.append(frame)
    # Type ignore ref: https://github.com/python/typeshed/pull/8244
    final_stack_summary = StackSummary.from_list(stack)
    tb_exc.stack = final_stack_summary
    for line in tb_exc.format():
        print(line, file=sys.stderr)
    return

