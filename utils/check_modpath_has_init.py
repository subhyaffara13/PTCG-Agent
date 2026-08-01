
def check_modpath_has_init(path: str, mod_path: list[str]) -> bool:
    """Check there are some __init__.py all along the way."""
    modpath: list[str] = []
    for part in mod_path:
        modpath.append(part)
        path = os.path.join(path, part)
        if not _has_init(path):
            old_namespace = util.is_namespace(".".join(modpath))
            if not old_namespace:
                return False
    return True

