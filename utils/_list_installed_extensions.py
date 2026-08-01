
def _list_installed_extensions() -> list[ExtensionManifest]:
    """Return manifests for all validly-installed extensions, sorted by directory name."""
    root_dir = EXTENSIONS_ROOT.expanduser()
    if not root_dir.is_dir():
        return []
    manifests = []
    for extension_dir in sorted(root_dir.iterdir()):
        if not extension_dir.is_dir() or not extension_dir.name.startswith("hf-"):
            continue
        try:
            manifests.append(ExtensionManifest.load(extension_dir))
        except Exception as e:
            logger.debug(f"Failed to load manifest for extension '{extension_dir.name}': {e}")
            continue
    return manifests

