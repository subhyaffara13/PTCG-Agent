
def find_imports_in_stream(
    input_stream: TextIO,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    unique: bool | ImportKey = False,
    top_only: bool = False,
    _seen: set[str] | None = None,
    **config_kwargs: Any,
) -> Iterator[identify.Import]:
    """Finds and returns all imports within the provided code stream.

    - **input_stream**: The stream of code with imports that need to be sorted.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **unique**: If True, only the first instance of an import is returned.
    - **top_only**: If True, only return imports that occur before the first function or class.
    - **_seen**: An optional set of imports already seen. Generally meant only for internal use.
    - ****config_kwargs**: Any config modifications.
    """
    config = _config(config=config, **config_kwargs)
    identified_imports = identify.imports(
        input_stream, config=config, file_path=file_path, top_only=top_only
    )
    if not unique:
        yield from identified_imports

    seen: set[str] = set() if _seen is None else _seen
    for identified_import in identified_imports:
        if unique in (True, ImportKey.ALIAS):
            key = identified_import.statement()
        elif unique == ImportKey.ATTRIBUTE:
            key = f"{identified_import.module}.{identified_import.attribute}"
        elif unique == ImportKey.MODULE:
            key = identified_import.module
        elif unique == ImportKey.PACKAGE:  # pragma: no branch # type checking ensures this
            key = identified_import.module.split(".")[0]

        if key and key not in seen:
            seen.add(key)
            yield identified_import

