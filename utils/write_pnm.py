
def write_pnm(file, width, height, pixels, meta):
    """Write a Netpbm PNM/PAM file."""

    bitdepth = meta["bitdepth"]
    maxval = 2**bitdepth - 1
    # Rudely, the number of image planes can be used to determine
    # whether we are L (PGM), LA (PAM), RGB (PPM), or RGBA (PAM).
    planes = meta["planes"]
    # Can be an assert as long as we assume that pixels and meta came
    # from a PNG file.
    assert planes in (1, 2, 3, 4)
    if planes in (1, 3):
        if 1 == planes:
            # PGM
            # Could generate PBM if maxval is 1, but we don't (for one
            # thing, we'd have to convert the data, not just blat it
            # out).
            fmt = "P5"
        else:
            # PPM
            fmt = "P6"
        file.write("%s %d %d %d\n" % (fmt, width, height, maxval))
    if planes in (2, 4):
        # PAM
        # See http://netpbm.sourceforge.net/doc/pam.html
        if 2 == planes:
            tupltype = "GRAYSCALE_ALPHA"
        else:
            tupltype = "RGB_ALPHA"
        file.write(
            "P7\nWIDTH %d\nHEIGHT %d\nDEPTH %d\nMAXVAL %d\n"
            "TUPLTYPE %s\nENDHDR\n" % (width, height, planes, maxval, tupltype)
        )
    # Values per row
    vpr = planes * width
    # struct format
    fmt = ">%d" % vpr
    if maxval > 0xFF:
        fmt = fmt + "H"
    else:
        fmt = fmt + "B"
    for row in pixels:
        file.write(struct.pack(fmt, *row))
    file.flush()

