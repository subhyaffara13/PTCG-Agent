
def file_from_modpath(
    modpath: list[str],
    path: Sequence[str] | None = None,
    context_file: str | None = None,
) -> str | None:
    return file_info_from_modpath(modpath, path, context_file).location

