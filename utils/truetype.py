
def truetype(
    font: StrOrBytesPath | BinaryIO,
    size: float = 10,
    index: int = 0,
    encoding: str = "",
    layout_engine: Layout | None = None,
) -> FreeTypeFont:
    """
    Load a TrueType or OpenType font from a file or file-like object,
    and create a font object. This function loads a font object from the given
    file or file-like object, and creates a font object for a font of the given
    size. For loading bitmap fonts instead, see :py:func:`~PIL.ImageFont.load`
    and :py:func:`~PIL.ImageFont.load_path`.

    Pillow uses FreeType to open font files. On Windows, be aware that FreeType
    will keep the file open as long as the FreeTypeFont object exists. Windows
    limits the number of files that can be open in C at once to 512, so if many
    fonts are opened simultaneously and that limit is approached, an
    ``OSError`` may be thrown, reporting that FreeType "cannot open resource".
    A workaround would be to copy the file(s) into memory, and open that instead.

    This function requires the _imagingft service.

    :param font: A filename or file-like object containing a TrueType font.
                 If the file is not found in this filename, the loader may also
                 search in other directories, such as:

                 * The :file:`fonts/` directory on Windows,
                 * :file:`/Library/Fonts/`, :file:`/System/Library/Fonts/`
                   and :file:`~/Library/Fonts/` on macOS.
                 * :file:`~/.local/share/fonts`, :file:`/usr/local/share/fonts`,
                   and :file:`/usr/share/fonts` on Linux; or those specified by
                   the ``XDG_DATA_HOME`` and ``XDG_DATA_DIRS`` environment variables
                   for user-installed and system-wide fonts, respectively.

    :param size: The requested size, in pixels.
    :param index: Which font face to load (default is first available face).
    :param encoding: Which font encoding to use (default is Unicode). Possible
                     encodings include (see the FreeType documentation for more
                     information):

                     * "unic" (Unicode)
                     * "symb" (Microsoft Symbol)
                     * "ADOB" (Adobe Standard)
                     * "ADBE" (Adobe Expert)
                     * "ADBC" (Adobe Custom)
                     * "armn" (Apple Roman)
                     * "sjis" (Shift JIS)
                     * "gb  " (PRC)
                     * "big5"
                     * "wans" (Extended Wansung)
                     * "joha" (Johab)
                     * "lat1" (Latin-1)

                     This specifies the character set to use. It does not alter the
                     encoding of any text provided in subsequent operations.
    :param layout_engine: Which layout engine to use, if available:
                     :attr:`.ImageFont.Layout.BASIC` or :attr:`.ImageFont.Layout.RAQM`.
                     If it is available, Raqm layout will be used by default.
                     Otherwise, basic layout will be used.

                     Raqm layout is recommended for all non-English text. If Raqm layout
                     is not required, basic layout will have better performance.

                     You can check support for Raqm layout using
                     :py:func:`PIL.features.check_feature` with ``feature="raqm"``.

                     .. versionadded:: 4.2.0
    :return: A font object.
    :exception OSError: If the file could not be read.
    :exception ValueError: If the font size is not greater than zero.
    """

    def freetype(font: StrOrBytesPath | BinaryIO) -> FreeTypeFont:
        return FreeTypeFont(font, size, index, encoding, layout_engine)

    try:
        return freetype(font)
    except OSError:
        if not is_path(font):
            raise
        ttf_filename = os.path.basename(font)

        dirs = []
        if sys.platform == "win32":
            # check the windows font repository
            # NOTE: must use uppercase WINDIR, to work around bugs in
            # 1.5.2's os.environ.get()
            windir = os.environ.get("WINDIR")
            if windir:
                dirs.append(os.path.join(windir, "fonts"))
        elif sys.platform in ("linux", "linux2"):
            data_home = os.environ.get("XDG_DATA_HOME")
            if not data_home:
                # The freedesktop spec defines the following default directory for
                # when XDG_DATA_HOME is unset or empty. This user-level directory
                # takes precedence over system-level directories.
                data_home = os.path.expanduser("~/.local/share")
            xdg_dirs = [data_home]

            data_dirs = os.environ.get("XDG_DATA_DIRS")
            if not data_dirs:
                # Similarly, defaults are defined for the system-level directories
                data_dirs = "/usr/local/share:/usr/share"
            xdg_dirs += data_dirs.split(":")

            dirs += [os.path.join(xdg_dir, "fonts") for xdg_dir in xdg_dirs]
        elif sys.platform == "darwin":
            dirs += [
                "/Library/Fonts",
                "/System/Library/Fonts",
                os.path.expanduser("~/Library/Fonts"),
            ]

        ext = os.path.splitext(ttf_filename)[1]
        first_font_with_a_different_extension = None
        for directory in dirs:
            for walkroot, walkdir, walkfilenames in os.walk(directory):
                for walkfilename in walkfilenames:
                    if ext and walkfilename == ttf_filename:
                        return freetype(os.path.join(walkroot, walkfilename))
                    elif not ext and os.path.splitext(walkfilename)[0] == ttf_filename:
                        fontpath = os.path.join(walkroot, walkfilename)
                        if os.path.splitext(fontpath)[1] == ".ttf":
                            return freetype(fontpath)
                        if not ext and first_font_with_a_different_extension is None:
                            first_font_with_a_different_extension = fontpath
        if first_font_with_a_different_extension:
            return freetype(first_font_with_a_different_extension)
        raise

