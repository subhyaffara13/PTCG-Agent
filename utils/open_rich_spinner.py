
def open_rich_spinner(label: str, console: Console | None = None) -> Generator[None]:
    if not logger.isEnabledFor(logging.INFO):
        # Don't show spinner if --quiet is given.
        yield
        return

    console = console or get_console()
    spinner = _PipRichSpinner(label)
    with Live(spinner, refresh_per_second=SPINS_PER_SECOND, console=console):
        try:
            yield
        except KeyboardInterrupt:
            spinner.finish("canceled")
            raise
        except Exception:
            spinner.finish("error")
            raise
        else:
            spinner.finish("done")

