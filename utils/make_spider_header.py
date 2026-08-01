
def makeSpiderHeader(im: Image.Image) -> list[bytes]:
    nsam, nrow = im.size
    lenbyt = max(1, nsam) * 4  # There are labrec records in the header
    labrec = int(1024 / lenbyt)
    if 1024 % lenbyt != 0:
        labrec += 1
    labbyt = labrec * lenbyt
    nvalues = int(labbyt / 4)
    if nvalues < 23:
        return []

    hdr = [0.0] * nvalues

    # NB these are Fortran indices
    hdr[1] = 1.0  # nslice (=1 for an image)
    hdr[2] = float(nrow)  # number of rows per slice
    hdr[3] = float(nrow)  # number of records in the image
    hdr[5] = 1.0  # iform for 2D image
    hdr[12] = float(nsam)  # number of pixels per line
    hdr[13] = float(labrec)  # number of records in file header
    hdr[22] = float(labbyt)  # total number of bytes in header
    hdr[23] = float(lenbyt)  # record length in bytes

    # adjust for Fortran indexing
    hdr = hdr[1:]
    hdr.append(0.0)
    # pack binary data into a string
    return [struct.pack("f", v) for v in hdr]

