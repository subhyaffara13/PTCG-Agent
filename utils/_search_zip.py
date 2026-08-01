
def _search_zip(
    modpath: tuple[str, ...],
) -> tuple[Literal[ModuleType.PY_ZIPMODULE], str, str]:
    for filepath, importer in _get_zipimporters():
        found = importer.find_spec(modpath[0])
        if found:
            if not importer.find_spec(os.path.sep.join(modpath)):
                raise ImportError(
                    "No module named {} in {}/{}".format(
                        ".".join(modpath[1:]), filepath, modpath
                    )
                )
            return (
                ModuleType.PY_ZIPMODULE,
                os.path.abspath(filepath) + os.path.sep + os.path.sep.join(modpath),
                filepath,
            )
    raise ImportError(f"No module named {'.'.join(modpath)}")

