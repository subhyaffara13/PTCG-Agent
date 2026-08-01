
def _update_converter():
    try:
        mpl._get_executable_info("magick")
    except mpl.ExecutableNotFoundError:
        pass
    else:
        converter['gif'] = _MagickConverter()
    try:
        mpl._get_executable_info("gs")
    except mpl.ExecutableNotFoundError:
        pass
    else:
        converter['pdf'] = converter['eps'] = _GSConverter()
    try:
        mpl._get_executable_info("inkscape")
    except mpl.ExecutableNotFoundError:
        pass
    else:
        converter['svg'] = _SVGConverter()

