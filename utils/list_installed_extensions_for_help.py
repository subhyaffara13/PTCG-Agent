
def list_installed_extensions_for_help() -> list[tuple[str, str]]:
    entries = []
    for manifest in _list_installed_extensions():
        tag = f"[extension {manifest.repo_id}]"
        help_text = f"{manifest.description} {tag}" if manifest.description is not None else tag
        entries.append((manifest.short_name, help_text))
    return entries

