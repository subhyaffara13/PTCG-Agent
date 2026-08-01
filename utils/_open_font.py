
def _open_font(path, master_finder=lambda s: s):
    # load TTFont masters from given 'path': this can be either a .TTX or an
    # OpenType binary font; or if neither of these, try use the 'master_finder'
    # callable to resolve the path to a valid .TTX or OpenType font binary.
    from fontTools.ttx import guessFileType

    master_path = os.path.normpath(path)
    tp = guessFileType(master_path)
    if tp is None:
        # not an OpenType binary/ttx, fall back to the master finder.
        master_path = master_finder(master_path)
        tp = guessFileType(master_path)
    if tp in ("TTX", "OTX"):
        font = TTFont()
        font.importXML(master_path)
    elif tp in ("TTF", "OTF", "WOFF", "WOFF2"):
        font = TTFont(master_path)
    else:
        raise VarLibValidationError("Invalid master path: %r" % master_path)
    return font

