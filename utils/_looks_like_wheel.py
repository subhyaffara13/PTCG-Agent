
def _looks_like_wheel(location: str) -> bool:
    if not location.endswith(WHEEL_EXTENSION):
        return False
    if not os.path.isfile(location):
        return False
    try:
        parse_wheel_filename(os.path.basename(location))
    except InvalidWheelFilename:
        return False
    return zipfile.is_zipfile(location)

