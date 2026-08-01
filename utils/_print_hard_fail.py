
def _print_hard_fail(
    config: Config, offending_file: str | None = None, message: str | None = None
) -> None:
    """Fail on unrecoverable exception with custom message."""
    message = message or (
        f"Unrecoverable exception thrown when parsing {offending_file or ''}! "
        "This should NEVER happen.\n"
        "If encountered, please open an issue: https://github.com/PyCQA/isort/issues/new"
    )
    printer = create_terminal_printer(
        color=config.color_output, error=config.format_error, success=config.format_success
    )
    printer.error(message)

