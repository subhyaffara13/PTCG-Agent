
def get_traceback(
    exc: BaseException,
    exception_config: DeveloperExceptionConfig,
    internal_dir_names: list[str],
) -> Traceback:
    rich_tb = Traceback.from_exception(
        type(exc),
        exc,
        exc.__traceback__,
        show_locals=exception_config.pretty_exceptions_show_locals,
        suppress=internal_dir_names,
        width=MAX_WIDTH,
        code_width=None,
        word_wrap=True,
    )
    return rich_tb


def get_traceback():
  return source_info_util.current().traceback

