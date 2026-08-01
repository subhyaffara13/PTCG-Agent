
def _raise_for_invalid_entrypoint(specification: str, scripts_dir: str) -> None:
    entry = get_export_entry(specification)
    if entry is None:
        return

    if entry.suffix is None:
        raise MissingCallableSuffix(str(entry))

    # distlib joins the entry point name onto the scripts directory, so a name
    # with path separators or ``..`` components can resolve elsewhere. The script
    # must resolve to a path strictly inside the scripts directory.
    dest = os.path.join(scripts_dir, entry.name)
    resolves_to_scripts_dir = os.path.abspath(dest) == os.path.abspath(scripts_dir)
    if resolves_to_scripts_dir or not is_within_directory(scripts_dir, dest):
        raise InstallationError(
            f"Invalid script entry point name {entry.name!r}: the script "
            f"would be installed outside the scripts directory ({scripts_dir})."
        )

