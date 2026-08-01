
def _is_legacy_zip_format(filename: str) -> bool:
    if zipfile.is_zipfile(filename):
        with zipfile.ZipFile(filename) as zf:
            infolist = zf.infolist()
        return len(infolist) == 1 and not infolist[0].is_dir()
    return False

