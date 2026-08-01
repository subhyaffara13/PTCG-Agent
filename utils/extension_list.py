
def extension_list() -> None:
    """List installed extension commands."""
    rows = [
        {
            "command": f"hf {manifest.short_name}",
            "source": str(manifest.repo_id),
            "type": str(manifest.type),
            "installed": manifest.installed_at.strftime("%Y-%m-%d"),
            "description": manifest.description,
        }
        for manifest in _list_installed_extensions()
    ]
    out.table(rows, id_key="command")

