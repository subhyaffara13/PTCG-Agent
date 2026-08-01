
def check_stream(
    input_stream: TextIO,
    show_diff: bool | TextIO = False,
    extension: str | None = None,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    disregard_skip: bool = False,
    **config_kwargs: Any,
) -> bool:
    """Checks any imports within the provided code stream, returning `False` if any unsorted or
    incorrectly imports are found or `True` if no problems are identified.

    - **input_stream**: The stream of code with imports that need to be sorted.
    - **show_diff**: If `True` the changes that need to be done will be printed to stdout, if a
    TextIO stream is provided results will be written to it, otherwise no diff will be computed.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **disregard_skip**: set to `True` if you want to ignore a skip set in config for this file.
    - ****config_kwargs**: Any config modifications.
    """
    config = _config(path=file_path, config=config, **config_kwargs)

    if show_diff:
        input_stream = StringIO(input_stream.read())

    changed: bool = sort_stream(
        input_stream=input_stream,
        output_stream=Empty,
        extension=extension,
        config=config,
        file_path=file_path,
        disregard_skip=disregard_skip,
    )
    printer = create_terminal_printer(
        color=config.color_output, error=config.format_error, success=config.format_success
    )
    if not changed:
        if config.verbose and not config.only_modified:
            printer.success(f"{file_path or ''} Everything Looks Good!")
        return True

    printer.error(f"{file_path or ''} Imports are incorrectly sorted and/or formatted.")
    if show_diff:
        output_stream = StringIO()
        input_stream.seek(0)
        file_contents = input_stream.read()
        sort_stream(
            input_stream=StringIO(file_contents),
            output_stream=output_stream,
            extension=extension,
            config=config,
            file_path=file_path,
            disregard_skip=disregard_skip,
        )
        output_stream.seek(0)

        show_unified_diff(
            file_input=file_contents,
            file_output=output_stream.read(),
            file_path=file_path,
            output=None if show_diff is True else show_diff,
            color_output=config.color_output,
        )
    return False

