from typing import Any
from pathlib import Path


def sort_code_string(
    code: str,
    extension: str | None = None,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    disregard_skip: bool = False,
    show_diff: bool | TextIO = False,
    **config_kwargs: Any,
) -> str:
    """Sorts any imports within the provided code string, returning a new string with them sorted.

    - **code**: The string of code with imports that need to be sorted.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **disregard_skip**: set to `True` if you want to ignore a skip set in config for this file.
    - **show_diff**: If `True` the changes that need to be done will be printed to stdout, if a
    TextIO stream is provided results will be written to it, otherwise no diff will be computed.
    - ****config_kwargs**: Any config modifications.
    """
    input_stream = StringIO(code)
    output_stream = StringIO()
    config = _config(path=file_path, config=config, **config_kwargs)
    sort_stream(
        input_stream,
        output_stream,
        extension=extension,
        config=config,
        file_path=file_path,
        disregard_skip=disregard_skip,
        show_diff=show_diff,
    )
    output_stream.seek(0)
    return output_stream.read()

