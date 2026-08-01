
def find_imports_in_file(
    filename: str | Path,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    unique: bool | ImportKey = False,
    top_only: bool = False,
    **config_kwargs: Any,
) -> Iterator[identify.Import]:
    """Finds and returns all imports within the provided source file.

    - **filename**: The name or Path of the file to look for imports in.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **unique**: If True, only the first instance of an import is returned.
    - **top_only**: If True, only return imports that occur before the first function or class.
    - ****config_kwargs**: Any config modifications.
    """
    try:
        with io.File.read(filename) as source_file:
            yield from find_imports_in_stream(
                input_stream=source_file.stream,
                config=config,
                file_path=file_path or source_file.path,
                unique=unique,
                top_only=top_only,
                **config_kwargs,
            )
    except OSError as error:
        warn(f"Unable to parse file {filename} due to {error}", stacklevel=2)

