
def sort_imports(
    file_name: str,
    config: Config,
    check: bool = False,
    ask_to_apply: bool = False,
    write_to_stdout: bool = False,
    **kwargs: Any,
) -> SortAttempt | None:
    incorrectly_sorted: bool = False
    skipped: bool = False
    try:
        if check:
            try:
                incorrectly_sorted = not api.check_file(file_name, config=config, **kwargs)
            except FileSkipped:
                skipped = True
            return SortAttempt(incorrectly_sorted, skipped, True)

        try:
            incorrectly_sorted = not api.sort_file(
                file_name,
                config=config,
                ask_to_apply=ask_to_apply,
                write_to_stdout=write_to_stdout,
                **kwargs,
            )
        except FileSkipped:
            skipped = True
        return SortAttempt(incorrectly_sorted, skipped, True)
    except (OSError, ValueError) as error:
        warn(f"Unable to parse file {file_name} due to {error}", stacklevel=2)
        return None
    except UnsupportedEncoding:
        if config.verbose:
            warn(f"Encoding not supported for {file_name}", stacklevel=2)
        return SortAttempt(incorrectly_sorted, skipped, False)
    except ISortError as error:
        _print_hard_fail(config, message=str(error))
        sys.exit(1)
    except Exception:
        _print_hard_fail(config, offending_file=file_name)
        raise

