
def make_pdf_to_png_converter():
    """Return a function that converts a pdf file to a png file."""
    try:
        mpl._get_executable_info("pdftocairo")
    except mpl.ExecutableNotFoundError:
        pass
    else:
        return lambda pdffile, pngfile, dpi: subprocess.check_output(
            ["pdftocairo", "-singlefile", "-transp", "-png", "-r", "%d" % dpi,
             pdffile, os.path.splitext(pngfile)[0]],
            stderr=subprocess.STDOUT)
    try:
        gs_info = mpl._get_executable_info("gs")
    except mpl.ExecutableNotFoundError:
        pass
    else:
        return lambda pdffile, pngfile, dpi: subprocess.check_output(
            [gs_info.executable,
             '-dQUIET', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-dNOPROMPT',
             '-dUseCIEColor', '-dTextAlphaBits=4',
             '-dGraphicsAlphaBits=4', '-dDOINTERPOLATE',
             '-sDEVICE=pngalpha', '-sOutputFile=%s' % pngfile,
             '-r%d' % dpi, pdffile],
            stderr=subprocess.STDOUT)
    raise RuntimeError("No suitable pdf to png renderer found.")

