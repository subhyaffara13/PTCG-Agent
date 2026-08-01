
def unpack_file(
    filename: str,
    location: str,
    content_type: str | None = None,
) -> None:
    """Unpack ``filename`` into ``location``.

    Archive format is chosen in order of decreasing reliability:
    ``content_type``, then filename extension, then magic signature
    (unambiguous matches only).
    """
    filename = os.path.realpath(filename)
    zip_flatten = not filename.endswith(".whl")

    def _unzip() -> None:
        unzip_file(filename, location, flatten=zip_flatten)

    def _untar() -> None:
        untar_file(filename, location)

    if content_type == "application/zip":
        return _unzip()
    if content_type == "application/x-gzip":
        return _untar()

    if filename.lower().endswith(ZIP_EXTENSIONS):
        return _unzip()
    if filename.lower().endswith(TAR_EXTENSIONS + BZ2_EXTENSIONS + XZ_EXTENSIONS):
        return _untar()

    # avoid ambiguous case where both signature checks return True
    is_zipfile = zipfile.is_zipfile(filename)
    is_tarfile = tarfile.is_tarfile(filename)
    if is_zipfile and not is_tarfile:
        return _unzip()
    if is_tarfile and not is_zipfile:
        return _untar()
    if is_zipfile and is_tarfile:
        logger.error("Ambiguous file signature in %s.", filename)

    logger.critical(
        "Cannot unpack file %s (downloaded from %s, content-type: %s); "
        "cannot detect archive format",
        filename,
        location,
        content_type,
    )
    raise InstallationError(f"Cannot determine archive format of {location}")

