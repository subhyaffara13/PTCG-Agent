
def is_silent_import_module(manager: BuildManager, path: str) -> bool:
    if manager.options.no_silence_site_packages:
        return False
    # Silence errors in site-package dirs and typeshed
    if any(is_sub_path_normabs(path, dir) for dir in manager.search_paths.package_path):
        return True
    return any(is_sub_path_normabs(path, dir) for dir in manager.search_paths.typeshed_path)

