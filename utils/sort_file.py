import sys
from typing import Any
from pathlib import Path


def sort_file(
    filename: str | Path,
    extension: str | None = None,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    disregard_skip: bool = True,
    ask_to_apply: bool = False,
    show_diff: bool | TextIO = False,
    write_to_stdout: bool = False,
    output: TextIO | None = None,
    **config_kwargs: Any,
) -> bool:
    """Sorts and formats any groups of imports within the provided file or Path.
     Returns `True` if the file has been changed, otherwise `False`.

    - **filename**: The name or Path of the file to format.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **disregard_skip**: set to `True` if you want to ignore a skip set in config for this file.
    - **ask_to_apply**: If `True`, prompt before applying any changes.
    - **show_diff**: If `True` the changes that need to be done will be printed to stdout, if a
    TextIO stream is provided results will be written to it, otherwise no diff will be computed.
    - **write_to_stdout**: If `True`, write to stdout instead of the input file.
    - **output**: If a TextIO is provided, results will be written there rather than replacing
    the original file content.
    - ****config_kwargs**: Any config modifications.
    """
    file_config: Config = config

    if "config_trie" in config_kwargs:
        config_trie = config_kwargs.pop("config_trie", None)
        if config_trie:
            config_info = config_trie.search(filename)
            if config.verbose:
                print(f"{config_info[0]} used for file {filename}")

            file_config = Config(**config_info[1])

    with io.File.read(filename) as source_file:
        actual_file_path = file_path or source_file.path
        config = _config(path=actual_file_path, config=file_config, **config_kwargs)
        changed: bool = False
        try:
            if write_to_stdout:
                changed = sort_stream(
                    input_stream=source_file.stream,
                    output_stream=sys.stdout,
                    config=config,
                    file_path=actual_file_path,
                    disregard_skip=disregard_skip,
                    extension=extension,
                )
            else:
                if output is None:
                    try:
                        if config.overwrite_in_place:
                            output_stream_context = _in_memory_output_stream_context()
                        else:
                            output_stream_context = _file_output_stream_context(
                                filename, source_file
                            )
                        with output_stream_context as output_stream:
                            changed = sort_stream(
                                input_stream=source_file.stream,
                                output_stream=output_stream,
                                config=config,
                                file_path=actual_file_path,
                                disregard_skip=disregard_skip,
                                extension=extension,
                            )
                            output_stream.seek(0)
                            if changed:
                                if show_diff or ask_to_apply:
                                    source_file.stream.seek(0)
                                    show_unified_diff(
                                        file_input=source_file.stream.read(),
                                        file_output=output_stream.read(),
                                        file_path=actual_file_path,
                                        output=(
                                            None if show_diff is True else cast(TextIO, show_diff)
                                        ),
                                        color_output=config.color_output,
                                    )
                                    if show_diff or (
                                        ask_to_apply
                                        and not ask_whether_to_apply_changes_to_file(
                                            str(source_file.path)
                                        )
                                    ):
                                        return False
                                source_file.stream.close()
                                if config.overwrite_in_place:
                                    output_stream.seek(0)
                                    with source_file.path.open("w") as fs:
                                        shutil.copyfileobj(output_stream, fs)
                        if changed:
                            if not config.overwrite_in_place:
                                tmp_file = _tmp_file(source_file)
                                tmp_file.replace(source_file.path)
                            if not config.quiet:
                                print(f"Fixing {source_file.path}")
                    finally:
                        if not config.overwrite_in_place:  # pragma: no branch
                            tmp_file = _tmp_file(source_file)
                            tmp_file.unlink(missing_ok=True)
                else:
                    changed = sort_stream(
                        input_stream=source_file.stream,
                        output_stream=output,
                        config=config,
                        file_path=actual_file_path,
                        disregard_skip=disregard_skip,
                        extension=extension,
                    )
                    if changed and show_diff:
                        source_file.stream.seek(0)
                        output.seek(0)
                        show_unified_diff(
                            file_input=source_file.stream.read(),
                            file_output=output.read(),
                            file_path=actual_file_path,
                            output=None if show_diff is True else show_diff,
                            color_output=config.color_output,
                        )
                    source_file.stream.close()

        except ExistingSyntaxErrors:
            warn(f"{actual_file_path} unable to sort due to existing syntax errors", stacklevel=2)
        except IntroducedSyntaxErrors:  # pragma: no cover
            warn(
                f"{actual_file_path} unable to sort as isort introduces new syntax errors",
                stacklevel=2,
            )

        return changed

