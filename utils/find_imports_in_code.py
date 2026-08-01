
def find_imports_in_code(
    code: str,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    unique: bool | ImportKey = False,
    top_only: bool = False,
    **config_kwargs: Any,
) -> Iterator[identify.Import]:
    """Finds and returns all imports within the provided code string.

    - **code**: The string of code with imports that need to be sorted.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **unique**: If True, only the first instance of an import is returned.
    - **top_only**: If True, only return imports that occur before the first function or class.
    - ****config_kwargs**: Any config modifications.
    """
    yield from find_imports_in_stream(
        input_stream=StringIO(code),
        config=config,
        file_path=file_path,
        unique=unique,
        top_only=top_only,
        **config_kwargs,
    )

