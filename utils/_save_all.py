import os

def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    _save(im, fp, filename, save_all=True)


def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    _save(im, fp, filename, save_all=True)


def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    append_images = im.encoderinfo.get("append_images", [])
    if not append_images and not getattr(im, "is_animated", False):
        _save(im, fp, filename)
        return

    mpf_offset = 28
    offsets: list[int] = []
    im_sequences = [im, *append_images]
    total = sum(getattr(seq, "n_frames", 1) for seq in im_sequences)
    for im_sequence in im_sequences:
        for im_frame in ImageSequence.Iterator(im_sequence):
            if not offsets:
                # APP2 marker
                ifd_length = 66 + 16 * total
                im_frame.encoderinfo["extra"] = (
                    b"\xff\xe2"
                    + struct.pack(">H", 6 + ifd_length)
                    + b"MPF\0"
                    + b" " * ifd_length
                )
                if exif := im_frame.encoderinfo.get("exif"):
                    if isinstance(exif, Image.Exif):
                        exif = exif.tobytes()
                        im_frame.encoderinfo["exif"] = exif
                    mpf_offset += 4 + len(exif)

                JpegImagePlugin._save(im_frame, fp, filename)
                offsets.append(fp.tell())
            else:
                encoderinfo = im_frame._attach_default_encoderinfo(im)
                im_frame.save(fp, "JPEG")
                im_frame.encoderinfo = encoderinfo
                offsets.append(fp.tell() - offsets[-1])

    ifd = TiffImagePlugin.ImageFileDirectory_v2()
    ifd[0xB000] = b"0100"
    ifd[0xB001] = len(offsets)

    mpentries = b""
    data_offset = 0
    for i, size in enumerate(offsets):
        if i == 0:
            mptype = 0x030000  # Baseline MP Primary Image
        else:
            mptype = 0x000000  # Undefined
        mpentries += struct.pack("<LLLHH", mptype, size, data_offset, 0, 0)
        if i == 0:
            data_offset -= mpf_offset
        data_offset += size
    ifd[0xB002] = mpentries

    fp.seek(mpf_offset)
    fp.write(b"II\x2a\x00" + o32le(8) + ifd.tobytes(8))
    fp.seek(0, os.SEEK_END)


def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    _save(im, fp, filename, save_all=True)


def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    _save(im, fp, filename, save_all=True)


def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    append_images = list(im.encoderinfo.get("append_images", []))
    if not hasattr(im, "n_frames") and not append_images:
        return _save(im, fp, filename)

    cur_idx = im.tell()
    try:
        with AppendingTiffWriter(fp) as tf:
            for ims in [im] + append_images:
                encoderinfo = ims._attach_default_encoderinfo(im)
                if not hasattr(ims, "encoderconfig"):
                    ims.encoderconfig = ()
                nfr = getattr(ims, "n_frames", 1)

                for idx in range(nfr):
                    ims.seek(idx)
                    ims.load()
                    _save(ims, tf, filename)
                    tf.newFrame()
                ims.encoderinfo = encoderinfo
    finally:
        im.seek(cur_idx)


def _save_all(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    encoderinfo = im.encoderinfo.copy()
    append_images = list(encoderinfo.get("append_images", []))

    # If total frame count is 1, then save using the legacy API, which
    # will preserve non-alpha modes
    total = 0
    for ims in [im] + append_images:
        total += getattr(ims, "n_frames", 1)
    if total == 1:
        _save(im, fp, filename)
        return

    background: int | tuple[int, ...] = (0, 0, 0, 0)
    if "background" in encoderinfo:
        background = encoderinfo["background"]
    elif "background" in im.info:
        background = im.info["background"]
        if isinstance(background, int):
            # GifImagePlugin stores a global color table index in
            # info["background"]. So it must be converted to an RGBA value
            palette = im.getpalette()
            if palette:
                r, g, b = palette[background * 3 : (background + 1) * 3]
                background = (r, g, b, 255)
            else:
                background = (background, background, background, 255)

    duration = im.encoderinfo.get("duration", im.info.get("duration", 0))
    loop = im.encoderinfo.get("loop", 0)
    minimize_size = im.encoderinfo.get("minimize_size", False)
    kmin = im.encoderinfo.get("kmin", None)
    kmax = im.encoderinfo.get("kmax", None)
    allow_mixed = im.encoderinfo.get("allow_mixed", False)
    verbose = False
    lossless = im.encoderinfo.get("lossless", False)
    quality = im.encoderinfo.get("quality", 80)
    alpha_quality = im.encoderinfo.get("alpha_quality", 100)
    method = im.encoderinfo.get("method", 0)
    icc_profile = im.encoderinfo.get("icc_profile") or ""
    exif = im.encoderinfo.get("exif", "")
    if isinstance(exif, Image.Exif):
        exif = exif.tobytes()
    xmp = im.encoderinfo.get("xmp", "")
    if allow_mixed:
        lossless = False

    # Sensible keyframe defaults are from gif2webp.c script
    if kmin is None:
        kmin = 9 if lossless else 3
    if kmax is None:
        kmax = 17 if lossless else 5

    # Validate background color
    if (
        not isinstance(background, (list, tuple))
        or len(background) != 4
        or not all(0 <= v < 256 for v in background)
    ):
        msg = f"Background color is not an RGBA tuple clamped to (0-255): {background}"
        raise OSError(msg)

    # Convert to packed uint
    bg_r, bg_g, bg_b, bg_a = background
    background = (bg_a << 24) | (bg_r << 16) | (bg_g << 8) | (bg_b << 0)

    # Setup the WebP animation encoder
    enc = _webp.WebPAnimEncoder(
        im.size,
        background,
        loop,
        minimize_size,
        kmin,
        kmax,
        allow_mixed,
        verbose,
    )

    # Add each frame
    frame_idx = 0
    timestamp = 0
    cur_idx = im.tell()
    try:
        for ims in [im] + append_images:
            # Get number of frames in this image
            nfr = getattr(ims, "n_frames", 1)

            for idx in range(nfr):
                ims.seek(idx)

                frame = _convert_frame(ims)

                # Append the frame to the animation encoder
                enc.add(
                    frame.getim(),
                    round(timestamp),
                    lossless,
                    quality,
                    alpha_quality,
                    method,
                )

                # Update timestamp and frame index
                if isinstance(duration, (list, tuple)):
                    timestamp += duration[frame_idx]
                else:
                    timestamp += duration
                frame_idx += 1

    finally:
        im.seek(cur_idx)

    # Force encoder to flush frames
    enc.add(None, round(timestamp), lossless, quality, alpha_quality, 0)

    # Get the final output from the encoder
    data = enc.assemble(icc_profile, exif, xmp)
    if data is None:
        msg = "cannot write file as WebP (encoder returned None)"
        raise OSError(msg)

    fp.write(data)

