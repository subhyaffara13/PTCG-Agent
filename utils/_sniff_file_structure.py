import os

def _sniffFileStructure(ufo_path: PathStr) -> UFOFileStructure:
    """Return UFOFileStructure.ZIP if the UFO at path 'ufo_path' (str)
    is a zip file, else return UFOFileStructure.PACKAGE if 'ufo_path' is a
    directory.
    Raise UFOLibError if it is a file with unknown structure, or if the path
    does not exist.
    """
    if zipfile.is_zipfile(ufo_path):
        return UFOFileStructure.ZIP
    elif os.path.isdir(ufo_path):
        return UFOFileStructure.PACKAGE
    elif os.path.isfile(ufo_path):
        raise UFOLibError(
            "The specified UFO does not have a known structure: '%s'" % ufo_path
        )
    else:
        raise UFOLibError("No such file or directory: '%s'" % ufo_path)

