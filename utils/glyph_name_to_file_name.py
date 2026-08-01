
def glyphNameToFileName(glyphName: str, existingFileNames: Optional[set[str]]) -> str:
    """
    Wrapper around the userNameToFileName function in filenames.py

    Note that existingFileNames should be a set for large glyphsets
    or performance will suffer.
    """
    if existingFileNames is None:
        existingFileNames = set()
    return userNameToFileName(glyphName, existing=existingFileNames, suffix=".glif")

