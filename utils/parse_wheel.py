
def parse_wheel(wheel_zip: ZipFile, name: str) -> tuple[str, Message]:
    """Extract information from the provided wheel, ensuring it meets basic
    standards.

    Returns the name of the .dist-info directory and the parsed WHEEL metadata.
    """
    try:
        info_dir = wheel_dist_info_dir(wheel_zip, name)
        metadata = wheel_metadata(wheel_zip, info_dir)
        version = wheel_version(metadata)
    except UnsupportedWheel as e:
        raise UnsupportedWheel(f"{name} has an invalid wheel, {e}")

    check_compatibility(version, name)

    return info_dir, metadata

