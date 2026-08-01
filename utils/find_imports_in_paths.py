
def find_imports_in_paths(
    paths: Iterator[str | Path],
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    unique: bool | ImportKey = False,
    top_only: bool = False,
    **config_kwargs: Any,
) -> Iterator[identify.Import]:
    """Finds and returns all imports within the provided source paths.

    - **paths**: A collection of paths to recursively look for imports within.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **unique**: If True, only the first instance of an import is returned.
    - **top_only**: If True, only return imports that occur before the first function or class.
    - ****config_kwargs**: Any config modifications.
    """
    config = _config(config=config, **config_kwargs)
    seen: set[str] | None = set() if unique else None
    yield from chain(
        *(
            find_imports_in_file(
                file_name, unique=unique, config=config, top_only=top_only, _seen=seen
            )
            for file_name in files.find(map(str, paths), config, [], [])
        )
    )

