
def check_code_string(
    code: str,
    show_diff: bool | TextIO = False,
    extension: str | None = None,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    disregard_skip: bool = False,
    **config_kwargs: Any,
) -> bool:
    """Checks the order, format, and categorization of imports within the provided code string.
    Returns `True` if everything is correct, otherwise `False`.

    - **code**: The string of code with imports that need to be sorted.
    - **show_diff**: If `True` the changes that need to be done will be printed to stdout, if a
    TextIO stream is provided results will be written to it, otherwise no diff will be computed.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **disregard_skip**: set to `True` if you want to ignore a skip set in config for this file.
    - ****config_kwargs**: Any config modifications.
    """
    config = _config(path=file_path, config=config, **config_kwargs)
    return check_stream(
        StringIO(code),
        show_diff=show_diff,
        extension=extension,
        config=config,
        file_path=file_path,
        disregard_skip=disregard_skip,
    )

