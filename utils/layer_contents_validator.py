
def layerContentsValidator(
    value: Any, ufoPathOrFileSystem: Union[str, fs.base.FS]
) -> tuple[bool, Optional[str]]:
    """
    Check the validity of layercontents.plist.
    Version 3+.
    """
    if isinstance(ufoPathOrFileSystem, fs.base.FS):
        fileSystem = ufoPathOrFileSystem
    else:
        fileSystem = fs.osfs.OSFS(ufoPathOrFileSystem)

    bogusFileMessage = "layercontents.plist in not in the correct format."
    # file isn't in the right format
    if not isinstance(value, list):
        return False, bogusFileMessage
    # work through each entry
    usedLayerNames = set()
    usedDirectories = set()
    contents = {}
    for entry in value:
        # layer entry in the incorrect format
        if not isinstance(entry, list):
            return False, bogusFileMessage
        if not len(entry) == 2:
            return False, bogusFileMessage
        for i in entry:
            if not isinstance(i, str):
                return False, bogusFileMessage
        layerName, directoryName = entry
        # check directory naming
        if directoryName != "glyphs":
            if not directoryName.startswith("glyphs."):
                return (
                    False,
                    "Invalid directory name (%s) in layercontents.plist."
                    % directoryName,
                )
        if len(layerName) == 0:
            return False, "Empty layer name in layercontents.plist."
        # directory doesn't exist
        if not fileSystem.exists(directoryName):
            return False, "A glyphset does not exist at %s." % directoryName
        # default layer name
        if layerName == "public.default" and directoryName != "glyphs":
            return (
                False,
                "The name public.default is being used by a layer that is not the default.",
            )
        # check usage
        if layerName in usedLayerNames:
            return (
                False,
                "The layer name %s is used by more than one layer." % layerName,
            )
        usedLayerNames.add(layerName)
        if directoryName in usedDirectories:
            return (
                False,
                "The directory %s is used by more than one layer." % directoryName,
            )
        usedDirectories.add(directoryName)
        # store
        contents[layerName] = directoryName
    # missing default layer
    foundDefault = "glyphs" in contents.values()
    if not foundDefault:
        return False, "The required default glyph set is not in the UFO."
    return True, None

