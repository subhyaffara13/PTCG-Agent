from typing import Any
from pathlib import Path


def sort_stream(
    input_stream: TextIO,
    output_stream: TextIO,
    extension: str | None = None,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    disregard_skip: bool = False,
    show_diff: bool | TextIO = False,
    raise_on_skip: bool = True,
    **config_kwargs: Any,
) -> bool:
    """Sorts any imports within the provided code stream, outputs to the provided output stream.
     Returns `True` if anything is modified from the original input stream, otherwise `False`.

    - **input_stream**: The stream of code with imports that need to be sorted.
    - **output_stream**: The stream where sorted imports should be written to.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **disregard_skip**: set to `True` if you want to ignore a skip set in config for this file.
    - **show_diff**: If `True` the changes that need to be done will be printed to stdout, if a
    TextIO stream is provided results will be written to it, otherwise no diff will be computed.
    - ****config_kwargs**: Any config modifications.
    """
    extension = extension or (file_path and file_path.suffix.lstrip(".")) or "py"
    if show_diff:
        _output_stream = StringIO()
        _input_stream = StringIO(input_stream.read())
        changed = sort_stream(
            input_stream=_input_stream,
            output_stream=_output_stream,
            extension=extension,
            config=config,
            file_path=file_path,
            disregard_skip=disregard_skip,
            raise_on_skip=raise_on_skip,
            **config_kwargs,
        )
        _output_stream.seek(0)
        _input_stream.seek(0)
        show_unified_diff(
            file_input=_input_stream.read(),
            file_output=_output_stream.read(),
            file_path=file_path,
            output=output_stream if show_diff is True else show_diff,
            color_output=config.color_output,
        )
        return changed

    config = _config(path=file_path, config=config, **config_kwargs)
    content_source = str(file_path or "Passed in content")
    if not disregard_skip and file_path and config.is_skipped(file_path):
        raise FileSkipSetting(content_source)

    _internal_output = output_stream

    if config.atomic:
        try:
            file_content = input_stream.read()
            compile(file_content, content_source, "exec", flags=0, dont_inherit=True)
        except SyntaxError:
            if extension not in CYTHON_EXTENSIONS:
                raise ExistingSyntaxErrors(content_source)
            if config.verbose:
                warn(
                    f"{content_source} Python AST errors found but ignored due to Cython extension",
                    stacklevel=2,
                )
        input_stream = StringIO(file_content)

        if not output_stream.readable():
            _internal_output = StringIO()

    try:
        changed = core.process(
            input_stream,
            _internal_output,
            extension=extension,
            config=config,
            raise_on_skip=raise_on_skip,
        )
    except FileSkipComment:
        raise FileSkipComment(content_source)

    if config.atomic:
        _internal_output.seek(0)
        try:
            compile(_internal_output.read(), content_source, "exec", flags=0, dont_inherit=True)
            _internal_output.seek(0)
        except SyntaxError:  # pragma: no cover
            if extension not in CYTHON_EXTENSIONS:
                raise IntroducedSyntaxErrors(content_source)
            if config.verbose:
                warn(
                    f"{content_source} Python AST errors found but ignored due to Cython extension",
                    stacklevel=2,
                )
        if _internal_output != output_stream:
            output_stream.write(_internal_output.read())

    return changed

