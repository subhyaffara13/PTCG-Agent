
def Ghostscript(
    tile: list[ImageFile._Tile],
    size: tuple[int, int],
    fp: IO[bytes],
    scale: int = 1,
    transparency: bool = False,
) -> Image.core.ImagingCore:
    """Render an image using Ghostscript"""
    global gs_binary
    if not has_ghostscript():
        msg = "Unable to locate Ghostscript on paths"
        raise OSError(msg)
    assert isinstance(gs_binary, str)

    # Unpack decoder tile
    args = tile[0].args
    assert isinstance(args, tuple)
    length, bbox = args

    # Hack to support hi-res rendering
    scale = int(scale) or 1
    width = size[0] * scale
    height = size[1] * scale
    # resolution is dependent on bbox and size
    res_x = 72.0 * width / (bbox[2] - bbox[0])
    res_y = 72.0 * height / (bbox[3] - bbox[1])

    out_fd, outfile = tempfile.mkstemp()
    os.close(out_fd)

    infile_temp = None
    if hasattr(fp, "name") and os.path.exists(fp.name):
        infile = fp.name
    else:
        in_fd, infile_temp = tempfile.mkstemp()
        os.close(in_fd)
        infile = infile_temp

        # Ignore length and offset!
        # Ghostscript can read it
        # Copy whole file to read in Ghostscript
        with open(infile_temp, "wb") as f:
            # fetch length of fp
            fp.seek(0, io.SEEK_END)
            fsize = fp.tell()
            # ensure start position
            # go back
            fp.seek(0)
            lengthfile = fsize
            while lengthfile > 0:
                s = fp.read(min(lengthfile, 100 * 1024))
                if not s:
                    break
                lengthfile -= len(s)
                f.write(s)

    if transparency:
        # "RGBA"
        device = "pngalpha"
    else:
        # "pnmraw" automatically chooses between
        # PBM ("1"), PGM ("L"), and PPM ("RGB").
        device = "pnmraw"

    # Build Ghostscript command
    command = [
        gs_binary,
        "-q",  # quiet mode
        f"-g{width:d}x{height:d}",  # set output geometry (pixels)
        f"-r{res_x:f}x{res_y:f}",  # set input DPI (dots per inch)
        "-dBATCH",  # exit after processing
        "-dNOPAUSE",  # don't pause between pages
        "-dSAFER",  # safe mode
        f"-sDEVICE={device}",
        f"-sOutputFile={outfile}",  # output file
        # adjust for image origin
        "-c",
        f"{-bbox[0]} {-bbox[1]} translate",
        "-f",
        infile,  # input file
        # showpage (see https://bugs.ghostscript.com/show_bug.cgi?id=698272)
        "-c",
        "showpage",
    ]

    # push data through Ghostscript
    try:
        startupinfo = None
        if sys.platform.startswith("win"):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.check_call(command, startupinfo=startupinfo)
        with Image.open(outfile) as out_im:
            out_im.load()
            return out_im.im.copy()
    finally:
        try:
            os.unlink(outfile)
            if infile_temp:
                os.unlink(infile_temp)
        except OSError:
            pass

