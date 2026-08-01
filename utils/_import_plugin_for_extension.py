
def _import_plugin_for_extension(ext: str | bytes) -> bool:
    """Import only the plugin needed for a specific file extension."""
    if not ext:
        return False

    if isinstance(ext, bytes):
        ext = ext.decode()
    ext = ext.lower()
    if ext in EXTENSION:
        return True

    plugin = _EXTENSION_PLUGIN.get(ext)
    if plugin is None:
        return False

    try:
        logger.debug("Importing %s", plugin)
        __import__(f"{__spec__.parent}.{plugin}", globals(), locals(), [])
        return True
    except ImportError as e:
        logger.debug("Image: failed to import %s: %s", plugin, e)
        return False

