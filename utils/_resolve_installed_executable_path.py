
def _resolve_installed_executable_path(short_name: str) -> Path:
    extension_dir = _get_extension_dir(short_name)
    manifest = ExtensionManifest.load(extension_dir)
    return Path(manifest.executable_path).expanduser()

