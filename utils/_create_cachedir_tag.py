
def _create_cachedir_tag(cache_dir: Path) -> None:
    """Create a CACHEDIR.TAG file in ``cache_dir`` if one does not already exist.

    The tag follows the `Cache Directory Tagging Standard <http://www.brynosaurus.com/cachedir/>`_
    so that backup tools can recognize and skip cache directories.
    """
    tag_path = cache_dir / "CACHEDIR.TAG"
    if not tag_path.exists():
        try:
            tag_path.write_text(CACHEDIR_TAG_CONTENT)
        except OSError:
            pass

