import itertools
import os
import pathlib
import sys
import time
from typing import Any, Callable

def _save(
    im: Image.Image, fp: IO[bytes], filename: str | bytes, save_all: bool = False
) -> None:
    info = im.encoderinfo.copy()
    if save_all:
        append_images = list(info.get("append_images", []))
    else:
        append_images = []

    grayscale_modes = {"1", "L", "I", "I;16", "I;16L", "I;16B", "I;16N", "F"}
    grayscale = all(
        frame.mode in grayscale_modes
        for ims in [im] + append_images
        for frame in ImageSequence.Iterator(ims)
    )

    quality = info.get("quality", 75)
    if not isinstance(quality, int) or quality < 0 or quality > 100:
        msg = "Invalid quality setting"
        raise ValueError(msg)

    duration = info.get("duration", 0)
    subsampling = info.get("subsampling", "4:0:0" if grayscale else "4:2:0")
    speed = info.get("speed", 6)
    max_threads = info.get("max_threads", _get_default_max_threads())
    codec = info.get("codec", "auto")
    if codec != "auto" and not _avif.encoder_codec_available(codec):
        msg = "Invalid saving codec"
        raise ValueError(msg)
    range_ = info.get("range", "full")
    tile_rows_log2 = info.get("tile_rows", 0)
    tile_cols_log2 = info.get("tile_cols", 0)
    alpha_premultiplied = bool(info.get("alpha_premultiplied", False))
    autotiling = bool(info.get("autotiling", tile_rows_log2 == tile_cols_log2 == 0))

    icc_profile = info.get("icc_profile", im.info.get("icc_profile"))
    exif_orientation = 1
    if exif := info.get("exif"):
        if isinstance(exif, Image.Exif):
            exif_data = exif
        else:
            exif_data = Image.Exif()
            exif_data.load(exif)
        if ExifTags.Base.Orientation in exif_data:
            exif_orientation = exif_data.pop(ExifTags.Base.Orientation)
            exif = exif_data.tobytes() if exif_data else b""
        elif isinstance(exif, Image.Exif):
            exif = exif_data.tobytes()

    xmp = info.get("xmp")

    if isinstance(xmp, str):
        xmp = xmp.encode("utf-8")

    advanced = info.get("advanced")
    if advanced is not None:
        if isinstance(advanced, dict):
            advanced = advanced.items()
        try:
            advanced = tuple(advanced)
        except TypeError:
            invalid = True
        else:
            invalid = any(not isinstance(v, tuple) or len(v) != 2 for v in advanced)
        if invalid:
            msg = (
                "advanced codec options must be a dict of key-value string "
                "pairs or a series of key-value two-tuples"
            )
            raise ValueError(msg)

    # Setup the AVIF encoder
    enc = _avif.AvifEncoder(
        im.size,
        subsampling,
        quality,
        speed,
        max_threads,
        codec,
        range_,
        tile_rows_log2,
        tile_cols_log2,
        alpha_premultiplied,
        autotiling,
        icc_profile or b"",
        exif or b"",
        exif_orientation,
        xmp or b"",
        advanced,
    )

    # Add each frame
    frame_idx = 0
    frame_duration = 0
    cur_idx = im.tell()
    is_single_frame = not append_images and not getattr(im, "is_animated", False)
    try:
        for ims in [im] + append_images:
            for frame in ImageSequence.Iterator(ims):
                # Make sure image mode is supported
                rawmode = frame.mode
                if ims.mode not in {"L", "RGB", "RGBA"}:
                    if ims.has_transparency_data:
                        rawmode = "RGBA"
                    elif ims.mode in grayscale_modes:
                        rawmode = "L"
                    else:
                        rawmode = "RGB"
                    frame = frame.convert(rawmode)

                # Update frame duration
                if isinstance(duration, (list, tuple)):
                    frame_duration = duration[frame_idx]
                else:
                    frame_duration = duration

                # Append the frame to the animation encoder
                enc.add(
                    frame.tobytes("raw", rawmode),
                    frame_duration,
                    frame.size,
                    rawmode,
                    is_single_frame,
                )

                # Update frame index
                frame_idx += 1

                if not save_all:
                    break

    finally:
        im.seek(cur_idx)

    # Get the final output from the encoder
    data = enc.finish()
    if data is None:
        msg = "cannot write file as AVIF (encoder returned None)"
        raise OSError(msg)

    fp.write(data)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode != "P":
        msg = "Unsupported BLP image mode"
        raise ValueError(msg)

    magic = b"BLP1" if im.encoderinfo.get("blp_version") == "BLP1" else b"BLP2"
    fp.write(magic)

    assert im.palette is not None
    fp.write(struct.pack("<i", 1))  # Uncompressed or DirectX compression

    alpha_depth = 1 if im.palette.mode == "RGBA" else 0
    if magic == b"BLP1":
        fp.write(struct.pack("<L", alpha_depth))
    else:
        fp.write(struct.pack("<b", Encoding.UNCOMPRESSED))
        fp.write(struct.pack("<b", alpha_depth))
        fp.write(struct.pack("<b", 0))  # alpha encoding
        fp.write(struct.pack("<b", 0))  # mips
    fp.write(struct.pack("<II", *im.size))
    if magic == b"BLP1":
        fp.write(struct.pack("<i", 5))
        fp.write(struct.pack("<i", 0))

    ImageFile._save(im, fp, [ImageFile._Tile("BLP", (0, 0) + im.size, 0, im.mode)])


def _save(
    im: Image.Image, fp: IO[bytes], filename: str | bytes, bitmap_header: bool = True
) -> None:
    try:
        rawmode, bits, colors = SAVE[im.mode]
    except KeyError as e:
        msg = f"cannot write mode {im.mode} as BMP"
        raise OSError(msg) from e

    info = im.encoderinfo

    dpi = info.get("dpi", (96, 96))

    # 1 meter == 39.3701 inches
    ppm = tuple(int(x * 39.3701 + 0.5) for x in dpi)

    stride = ((im.size[0] * bits + 7) // 8 + 3) & (~3)
    header = 40  # or 64 for OS/2 version 2
    image = stride * im.size[1]

    if im.mode == "1":
        palette = b"".join(o8(i) * 3 + b"\x00" for i in (0, 255))
    elif im.mode == "L":
        palette = b"".join(o8(i) * 3 + b"\x00" for i in range(256))
    elif im.mode == "P":
        palette = im.im.getpalette("RGB", "BGRX")
        colors = len(palette) // 4
    else:
        palette = None

    # bitmap header
    if bitmap_header:
        offset = 14 + header + colors * 4
        file_size = offset + image
        if file_size > 2**32 - 1:
            msg = "File size is too large for the BMP format"
            raise ValueError(msg)
        fp.write(
            b"BM"  # file type (magic)
            + o32(file_size)  # file size
            + o32(0)  # reserved
            + o32(offset)  # image data offset
        )

    # bitmap info header
    fp.write(
        o32(header)  # info header size
        + o32(im.size[0])  # width
        + o32(im.size[1])  # height
        + o16(1)  # planes
        + o16(bits)  # depth
        + o32(0)  # compression (0=uncompressed)
        + o32(image)  # size of bitmap
        + o32(ppm[0])  # resolution
        + o32(ppm[1])  # resolution
        + o32(colors)  # colors used
        + o32(colors)  # colors important
    )

    fp.write(b"\0" * (header - 40))  # padding (for OS/2 format)

    if palette:
        fp.write(palette)

    ImageFile._save(
        im, fp, [ImageFile._Tile("raw", (0, 0) + im.size, 0, (rawmode, stride, -1))]
    )


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if _handler is None or not hasattr(_handler, "save"):
        msg = "BUFR save handler not installed"
        raise OSError(msg)
    _handler.save(im, fp, filename)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode not in ("RGB", "RGBA", "L", "LA"):
        msg = f"cannot write mode {im.mode} as DDS"
        raise OSError(msg)

    flags = DDSD.CAPS | DDSD.HEIGHT | DDSD.WIDTH | DDSD.PIXELFORMAT
    bitcount = len(im.getbands()) * 8
    pixel_format = im.encoderinfo.get("pixel_format")
    args: tuple[int] | str
    if pixel_format:
        codec_name = "bcn"
        flags |= DDSD.LINEARSIZE
        pitch = (im.width + 3) * 4
        rgba_mask = [0, 0, 0, 0]
        pixel_flags = DDPF.FOURCC
        if pixel_format == "DXT1":
            fourcc = D3DFMT.DXT1
            args = (1,)
        elif pixel_format == "DXT3":
            fourcc = D3DFMT.DXT3
            args = (2,)
        elif pixel_format == "DXT5":
            fourcc = D3DFMT.DXT5
            args = (3,)
        else:
            fourcc = D3DFMT.DX10
            if pixel_format == "BC2":
                args = (2,)
                dxgi_format = DXGI_FORMAT.BC2_TYPELESS
            elif pixel_format == "BC3":
                args = (3,)
                dxgi_format = DXGI_FORMAT.BC3_TYPELESS
            elif pixel_format == "BC5":
                args = (5,)
                dxgi_format = DXGI_FORMAT.BC5_TYPELESS
                if im.mode != "RGB":
                    msg = "only RGB mode can be written as BC5"
                    raise OSError(msg)
            else:
                msg = f"cannot write pixel format {pixel_format}"
                raise OSError(msg)
    else:
        codec_name = "raw"
        flags |= DDSD.PITCH
        pitch = (im.width * bitcount + 7) // 8

        alpha = im.mode[-1] == "A"
        if im.mode[0] == "L":
            pixel_flags = DDPF.LUMINANCE
            args = im.mode
            if alpha:
                rgba_mask = [0x000000FF, 0x000000FF, 0x000000FF]
            else:
                rgba_mask = [0xFF000000, 0xFF000000, 0xFF000000]
        else:
            pixel_flags = DDPF.RGB
            args = im.mode[::-1]
            rgba_mask = [0x00FF0000, 0x0000FF00, 0x000000FF]

            if alpha:
                r, g, b, a = im.split()
                im = Image.merge("RGBA", (a, r, g, b))
        if alpha:
            pixel_flags |= DDPF.ALPHAPIXELS
        rgba_mask.append(0xFF000000 if alpha else 0)

        fourcc = D3DFMT.UNKNOWN
    fp.write(
        o32(DDS_MAGIC)
        + struct.pack(
            "<7I",
            124,  # header size
            flags,  # flags
            im.height,
            im.width,
            pitch,
            0,  # depth
            0,  # mipmaps
        )
        + struct.pack("11I", *((0,) * 11))  # reserved
        # pfsize, pfflags, fourcc, bitcount
        + struct.pack("<4I", 32, pixel_flags, fourcc, bitcount)
        + struct.pack("<4I", *rgba_mask)  # dwRGBABitMask
        + struct.pack("<5I", DDSCAPS.TEXTURE, 0, 0, 0, 0)
    )
    if fourcc == D3DFMT.DX10:
        fp.write(
            # dxgi_format, 2D resource, misc, array size, straight alpha
            struct.pack("<5I", dxgi_format, 3, 0, 0, 1)
        )
    ImageFile._save(im, fp, [ImageFile._Tile(codec_name, (0, 0) + im.size, 0, args)])


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes, eps: int = 1) -> None:
    """EPS Writer for the Python Imaging Library."""

    # make sure image data is available
    im.load()

    # determine PostScript image mode
    if im.mode == "L":
        operator = (8, 1, b"image")
    elif im.mode == "RGB":
        operator = (8, 3, b"false 3 colorimage")
    elif im.mode == "CMYK":
        operator = (8, 4, b"false 4 colorimage")
    else:
        msg = "image mode is not supported"
        raise ValueError(msg)

    if eps:
        # write EPS header
        fp.write(b"%!PS-Adobe-3.0 EPSF-3.0\n")
        fp.write(b"%%Creator: PIL 0.1 EpsEncode\n")
        # fp.write("%%CreationDate: %s"...)
        fp.write(b"%%%%BoundingBox: 0 0 %d %d\n" % im.size)
        fp.write(b"%%Pages: 1\n")
        fp.write(b"%%EndComments\n")
        fp.write(b"%%Page: 1 1\n")
        fp.write(b"%%ImageData: %d %d " % im.size)
        fp.write(b'%d %d 0 1 1 "%s"\n' % operator)

    # image header
    fp.write(b"gsave\n")
    fp.write(b"10 dict begin\n")
    fp.write(b"/buf %d string def\n" % (im.size[0] * operator[1]))
    fp.write(b"%d %d scale\n" % im.size)
    fp.write(b"%d %d 8\n" % im.size)  # <= bits
    fp.write(b"[%d 0 0 -%d 0 %d]\n" % (im.size[0], im.size[1], im.size[1]))
    fp.write(b"{ currentfile buf readhexstring pop } bind\n")
    fp.write(operator[2] + b"\n")
    if hasattr(fp, "flush"):
        fp.flush()

    ImageFile._save(im, fp, [ImageFile._Tile("eps", (0, 0) + im.size)])

    fp.write(b"\n%%%%EndBinary\n")
    fp.write(b"grestore end\n")
    if hasattr(fp, "flush"):
        fp.flush()


def _save(
    im: Image.Image, fp: IO[bytes], filename: str | bytes, save_all: bool = False
) -> None:
    # header
    if "palette" in im.encoderinfo or "palette" in im.info:
        palette = im.encoderinfo.get("palette", im.info.get("palette"))
    else:
        palette = None
        im.encoderinfo.setdefault("optimize", True)

    if not save_all or not _write_multiple_frames(im, fp, palette):
        _write_single_frame(im, fp, palette)

    fp.write(b";")  # end of file

    if hasattr(fp, "flush"):
        fp.flush()


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if _handler is None or not hasattr(_handler, "save"):
        msg = "GRIB save handler not installed"
        raise OSError(msg)
    _handler.save(im, fp, filename)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if _handler is None or not hasattr(_handler, "save"):
        msg = "HDF5 save handler not installed"
        raise OSError(msg)
    _handler.save(im, fp, filename)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    """
    Saves the image as a series of PNG files,
    that are then combined into a .icns file.
    """
    if hasattr(fp, "flush"):
        fp.flush()

    sizes = {
        b"ic07": 128,
        b"ic08": 256,
        b"ic09": 512,
        b"ic10": 1024,
        b"ic11": 32,
        b"ic12": 64,
        b"ic13": 256,
        b"ic14": 512,
    }
    provided_images = {im.width: im for im in im.encoderinfo.get("append_images", [])}
    size_streams = {}
    for size in set(sizes.values()):
        image = (
            provided_images[size]
            if size in provided_images
            else im.resize((size, size))
        )

        temp = io.BytesIO()
        image.save(temp, "png")
        size_streams[size] = temp.getvalue()

    entries = []
    for type, size in sizes.items():
        stream = size_streams[size]
        entries.append((type, HEADERSIZE + len(stream), stream))

    # Header
    fp.write(MAGIC)
    file_length = HEADERSIZE  # Header
    file_length += HEADERSIZE + 8 * len(entries)  # TOC
    file_length += sum(entry[1] for entry in entries)
    fp.write(struct.pack(">i", file_length))

    # TOC
    fp.write(b"TOC ")
    fp.write(struct.pack(">i", HEADERSIZE + len(entries) * HEADERSIZE))
    for entry in entries:
        fp.write(entry[0])
        fp.write(struct.pack(">i", entry[1]))

    # Data
    for entry in entries:
        fp.write(entry[0])
        fp.write(struct.pack(">i", entry[1]))
        fp.write(entry[2])

    if hasattr(fp, "flush"):
        fp.flush()


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    fp.write(_MAGIC)  # (2+2)
    bmp = im.encoderinfo.get("bitmap_format") == "bmp"
    sizes = im.encoderinfo.get(
        "sizes",
        [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    frames = []
    provided_ims = [im] + im.encoderinfo.get("append_images", [])
    width, height = im.size
    for size in sorted(set(sizes)):
        if size[0] > width or size[1] > height or size[0] > 256 or size[1] > 256:
            continue

        for provided_im in provided_ims:
            if provided_im.size != size:
                continue
            frames.append(provided_im)
            if bmp:
                bits = BmpImagePlugin.SAVE[provided_im.mode][1]
                bits_used = [bits]
                for other_im in provided_ims:
                    if other_im.size != size:
                        continue
                    bits = BmpImagePlugin.SAVE[other_im.mode][1]
                    if bits not in bits_used:
                        # Another image has been supplied for this size
                        # with a different bit depth
                        frames.append(other_im)
                        bits_used.append(bits)
            break
        else:
            # TODO: invent a more convenient method for proportional scalings
            frame = provided_im.copy()
            frame.thumbnail(size, Image.Resampling.LANCZOS, reducing_gap=None)
            frames.append(frame)
    fp.write(o16(len(frames)))  # idCount(2)
    offset = fp.tell() + len(frames) * 16
    for frame in frames:
        width, height = frame.size
        # 0 means 256
        fp.write(o8(width if width < 256 else 0))  # bWidth(1)
        fp.write(o8(height if height < 256 else 0))  # bHeight(1)

        bits, colors = BmpImagePlugin.SAVE[frame.mode][1:] if bmp else (32, 0)
        fp.write(o8(colors))  # bColorCount(1)
        fp.write(b"\0")  # bReserved(1)
        fp.write(b"\0\0")  # wPlanes(2)
        fp.write(o16(bits))  # wBitCount(2)

        image_io = BytesIO()
        if bmp:
            frame.save(image_io, "dib")

            if bits != 32:
                and_mask = Image.new("1", size)
                ImageFile._save(
                    and_mask,
                    image_io,
                    [ImageFile._Tile("raw", (0, 0) + size, 0, ("1", 0, -1))],
                )
        else:
            frame.save(image_io, "png")
        image_io.seek(0)
        image_bytes = image_io.read()
        if bmp:
            image_bytes = image_bytes[:8] + o32(height * 2) + image_bytes[12:]
        bytes_len = len(image_bytes)
        fp.write(o32(bytes_len))  # dwBytesInRes(4)
        fp.write(o32(offset))  # dwImageOffset(4)
        current = fp.tell()
        fp.seek(offset)
        fp.write(image_bytes)
        offset = offset + bytes_len
        fp.seek(current)


def _save(im: Image.Image, fp: IO[bytes], tile: list[_Tile], bufsize: int = 0) -> None:
    """Helper to save image based on tile list

    :param im: Image object.
    :param fp: File object.
    :param tile: Tile list.
    :param bufsize: Optional buffer size
    """

    im.load()
    if not hasattr(im, "encoderconfig"):
        im.encoderconfig = ()
    tile.sort(key=_tilesort)
    # FIXME: make MAXBLOCK a configuration parameter
    # It would be great if we could have the encoder specify what it needs
    # But, it would need at least the image size in most cases. RawEncode is
    # a tricky case.
    bufsize = max(MAXBLOCK, bufsize, im.size[0] * 4)  # see RawEncode.c
    try:
        fh = fp.fileno()
        fp.flush()
        _encode_tile(im, fp, tile, bufsize, fh)
    except (AttributeError, io.UnsupportedOperation) as exc:
        _encode_tile(im, fp, tile, bufsize, None, exc)
    if hasattr(fp, "flush"):
        fp.flush()


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    try:
        image_type, rawmode = SAVE[im.mode]
    except KeyError as e:
        msg = f"Cannot save {im.mode} images as IM"
        raise ValueError(msg) from e

    frames = im.encoderinfo.get("frames", 1)

    fp.write(f"Image type: {image_type} image\r\n".encode("ascii"))
    if filename:
        # Each line must be 100 characters or less,
        # or: SyntaxError("not an IM file")
        # 8 characters are used for "Name: " and "\r\n"
        # Keep just the filename, ditch the potentially overlong path
        if isinstance(filename, bytes):
            filename = filename.decode("ascii")
        name, ext = os.path.splitext(os.path.basename(filename))
        name = "".join([name[: 92 - len(ext)], ext])

        fp.write(f"Name: {name}\r\n".encode("ascii"))
    fp.write(f"Image size (x*y): {im.size[0]}*{im.size[1]}\r\n".encode("ascii"))
    fp.write(f"File size (no of images): {frames}\r\n".encode("ascii"))
    if im.mode in ["P", "PA"]:
        fp.write(b"Lut: 1\r\n")
    fp.write(b"\000" * (511 - fp.tell()) + b"\032")
    if im.mode in ["P", "PA"]:
        im_palette = im.im.getpalette("RGB", "RGB;L")
        colors = len(im_palette) // 3
        palette = b""
        for i in range(3):
            palette += im_palette[colors * i : colors * (i + 1)]
            palette += b"\x00" * (256 - colors)
        fp.write(palette)  # 768 bytes
    ImageFile._save(
        im, fp, [ImageFile._Tile("raw", (0, 0) + im.size, 0, (rawmode, 0, -1))]
    )


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    # Get the keyword arguments
    info = im.encoderinfo

    if isinstance(filename, str):
        filename = filename.encode()
    if filename.endswith(b".j2k") or info.get("no_jp2", False):
        kind = "j2k"
    else:
        kind = "jp2"

    offset = info.get("offset", None)
    tile_offset = info.get("tile_offset", None)
    tile_size = info.get("tile_size", None)
    quality_mode = info.get("quality_mode", "rates")
    quality_layers = info.get("quality_layers", None)
    if quality_layers is not None and not (
        isinstance(quality_layers, (list, tuple))
        and all(
            isinstance(quality_layer, (int, float)) for quality_layer in quality_layers
        )
    ):
        msg = "quality_layers must be a sequence of numbers"
        raise ValueError(msg)

    num_resolutions = info.get("num_resolutions", 0)
    cblk_size = info.get("codeblock_size", None)
    precinct_size = info.get("precinct_size", None)
    irreversible = info.get("irreversible", False)
    progression = info.get("progression", "LRCP")
    cinema_mode = info.get("cinema_mode", "no")
    mct = info.get("mct", 0)
    signed = info.get("signed", False)
    comment = info.get("comment")
    if isinstance(comment, str):
        comment = comment.encode()
    plt = info.get("plt", False)

    fd = -1
    if hasattr(fp, "fileno"):
        try:
            fd = fp.fileno()
        except Exception:
            fd = -1

    im.encoderconfig = (
        offset,
        tile_offset,
        tile_size,
        quality_mode,
        quality_layers,
        num_resolutions,
        cblk_size,
        precinct_size,
        irreversible,
        progression,
        cinema_mode,
        mct,
        signed,
        fd,
        comment,
        plt,
    )

    ImageFile._save(im, fp, [ImageFile._Tile("jpeg2k", (0, 0) + im.size, 0, kind)])


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    try:
        rawmode = RAWMODE[im.mode]
    except KeyError as e:
        msg = f"cannot write mode {im.mode} as JPEG"
        raise OSError(msg) from e

    info = im.encoderinfo

    dpi = [round(x) for x in info.get("dpi", (0, 0))]

    quality = info.get("quality", -1)
    subsampling = info.get("subsampling", -1)
    qtables = info.get("qtables")

    if quality == "keep":
        quality = -1
        subsampling = "keep"
        qtables = "keep"
    elif quality in presets:
        preset = presets[quality]
        quality = -1
        subsampling = preset.get("subsampling", -1)
        qtables = preset.get("quantization")
    elif not isinstance(quality, int):
        msg = "Invalid quality setting"
        raise ValueError(msg)
    else:
        if subsampling in presets:
            subsampling = presets[subsampling].get("subsampling", -1)
        if isinstance(qtables, str) and qtables in presets:
            qtables = presets[qtables].get("quantization")

    if subsampling == "4:4:4":
        subsampling = 0
    elif subsampling == "4:2:2":
        subsampling = 1
    elif subsampling == "4:2:0":
        subsampling = 2
    elif subsampling == "4:1:1":
        # For compatibility. Before Pillow 4.3, 4:1:1 actually meant 4:2:0.
        # Set 4:2:0 if someone is still using that value.
        subsampling = 2
    elif subsampling == "keep":
        if im.format != "JPEG":
            msg = "Cannot use 'keep' when original image is not a JPEG"
            raise ValueError(msg)
        subsampling = get_sampling(im)

    def validate_qtables(
        qtables: (
            str | tuple[list[int], ...] | list[list[int]] | dict[int, list[int]] | None
        ),
    ) -> list[list[int]] | None:
        if qtables is None:
            return qtables
        if isinstance(qtables, str):
            try:
                lines = [
                    int(num)
                    for line in qtables.splitlines()
                    for num in line.split("#", 1)[0].split()
                ]
            except ValueError as e:
                msg = "Invalid quantization table"
                raise ValueError(msg) from e
            else:
                qtables = [lines[s : s + 64] for s in range(0, len(lines), 64)]
        if isinstance(qtables, (tuple, list, dict)):
            if isinstance(qtables, dict):
                qtables = [
                    qtables[key] for key in range(len(qtables)) if key in qtables
                ]
            elif isinstance(qtables, tuple):
                qtables = list(qtables)
            if not (0 < len(qtables) < 5):
                msg = "None or too many quantization tables"
                raise ValueError(msg)
            try:
                for idx, table in enumerate(qtables):
                    if len(table) != 64:
                        msg = "Invalid quantization table"
                        raise TypeError(msg)
                    qtables[idx] = list(array.array("H", table))
            except TypeError as e:
                msg = "Invalid quantization table"
                raise ValueError(msg) from e
            return qtables

    if qtables == "keep":
        if im.format != "JPEG":
            msg = "Cannot use 'keep' when original image is not a JPEG"
            raise ValueError(msg)
        qtables = getattr(im, "quantization", None)
    qtables = validate_qtables(qtables)

    extra = info.get("extra", b"")

    MAX_BYTES_IN_MARKER = 65533
    if xmp := info.get("xmp"):
        overhead_len = 29  # b"http://ns.adobe.com/xap/1.0/\x00"
        max_data_bytes_in_marker = MAX_BYTES_IN_MARKER - overhead_len
        if len(xmp) > max_data_bytes_in_marker:
            msg = "XMP data is too long"
            raise ValueError(msg)
        size = o16(2 + overhead_len + len(xmp))
        extra += b"\xff\xe1" + size + b"http://ns.adobe.com/xap/1.0/\x00" + xmp

    if icc_profile := info.get("icc_profile"):
        overhead_len = 14  # b"ICC_PROFILE\0" + o8(i) + o8(len(markers))
        max_data_bytes_in_marker = MAX_BYTES_IN_MARKER - overhead_len
        markers = []
        while icc_profile:
            markers.append(icc_profile[:max_data_bytes_in_marker])
            icc_profile = icc_profile[max_data_bytes_in_marker:]
        i = 1
        for marker in markers:
            size = o16(2 + overhead_len + len(marker))
            extra += (
                b"\xff\xe2"
                + size
                + b"ICC_PROFILE\0"
                + o8(i)
                + o8(len(markers))
                + marker
            )
            i += 1

    comment = info.get("comment", im.info.get("comment"))

    # "progressive" is the official name, but older documentation
    # says "progression"
    # FIXME: issue a warning if the wrong form is used (post-1.1.7)
    progressive = info.get("progressive", False) or info.get("progression", False)

    optimize = info.get("optimize", False)

    exif = info.get("exif", b"")
    if isinstance(exif, Image.Exif):
        exif = exif.tobytes()
    if len(exif) > MAX_BYTES_IN_MARKER:
        msg = "EXIF data is too long"
        raise ValueError(msg)

    # get keyword arguments
    im.encoderconfig = (
        quality,
        progressive,
        info.get("smooth", 0),
        optimize,
        info.get("keep_rgb", False),
        info.get("streamtype", 0),
        dpi,
        subsampling,
        info.get("restart_marker_blocks", 0),
        info.get("restart_marker_rows", 0),
        qtables,
        comment,
        extra,
        exif,
    )

    # if we optimize, libjpeg needs a buffer big enough to hold the whole image
    # in a shot. Guessing on the size, at im.size bytes. (raw pixel size is
    # channels*size, this is a value that's been used in a django patch.
    # https://github.com/matthewwithanm/django-imagekit/issues/50
    if optimize or progressive:
        # CMYK can be bigger
        if im.mode == "CMYK":
            bufsize = 4 * im.size[0] * im.size[1]
        # keep sets quality to -1, but the actual value may be high.
        elif quality >= 95 or quality == -1:
            bufsize = 2 * im.size[0] * im.size[1]
        else:
            bufsize = im.size[0] * im.size[1]
        if exif:
            bufsize += len(exif) + 5
        if extra:
            bufsize += len(extra) + 1
    else:
        # The EXIF info needs to be written as one block, + APP1, + one spare byte.
        # Ensure that our buffer is big enough. Same with the icc_profile block.
        bufsize = max(len(exif) + 5, len(extra) + 1)

    ImageFile._save(
        im, fp, [ImageFile._Tile("jpeg", (0, 0) + im.size, 0, rawmode)], bufsize
    )


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    JpegImagePlugin._save(im, fp, filename)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode != "1":
        msg = f"cannot write mode {im.mode} as MSP"
        raise OSError(msg)

    # create MSP header
    header = [0] * 16

    header[0], header[1] = i16(b"Da"), i16(b"nM")  # version 1
    header[2], header[3] = im.size
    header[4], header[5] = 1, 1
    header[6], header[7] = 1, 1
    header[8], header[9] = im.size

    checksum = 0
    for h in header:
        checksum = checksum ^ h
    header[12] = checksum  # FIXME: is this the right field?

    # header
    for h in header:
        fp.write(o16(h))

    # image body
    ImageFile._save(im, fp, [ImageFile._Tile("raw", (0, 0) + im.size, 32, "1")])


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode == "P":
        rawmode = "P"
        bpp = 8
        version = 1

    elif im.mode == "L":
        if im.encoderinfo.get("bpp") in (1, 2, 4):
            # this is 8-bit grayscale, so we shift it to get the high-order bits,
            # and invert it because
            # Palm does grayscale from white (0) to black (1)
            bpp = im.encoderinfo["bpp"]
            maxval = (1 << bpp) - 1
            shift = 8 - bpp
            im = im.point(lambda x: maxval - (x >> shift))
        elif im.info.get("bpp") in (1, 2, 4):
            # here we assume that even though the inherent mode is 8-bit grayscale,
            # only the lower bpp bits are significant.
            # We invert them to match the Palm.
            bpp = im.info["bpp"]
            maxval = (1 << bpp) - 1
            im = im.point(lambda x: maxval - (x & maxval))
        else:
            msg = f"cannot write mode {im.mode} as Palm"
            raise OSError(msg)

        # we ignore the palette here
        im._mode = "P"
        rawmode = f"P;{bpp}"
        version = 1

    elif im.mode == "1":
        # monochrome -- write it inverted, as is the Palm standard
        rawmode = "1;I"
        bpp = 1
        version = 0

    else:
        msg = f"cannot write mode {im.mode} as Palm"
        raise OSError(msg)

    #
    # make sure image data is available
    im.load()

    # write header

    cols = im.size[0]
    rows = im.size[1]

    rowbytes = int((cols + (16 // bpp - 1)) / (16 // bpp)) * 2
    transparent_index = 0
    compression_type = _COMPRESSION_TYPES["none"]

    flags = 0
    if im.mode == "P":
        flags |= _FLAGS["custom-colormap"]
        colormap = im.im.getpalette()
        colors = len(colormap) // 3
        colormapsize = 4 * colors + 2
    else:
        colormapsize = 0

    if "offset" in im.info:
        offset = (rowbytes * rows + 16 + 3 + colormapsize) // 4
    else:
        offset = 0

    fp.write(o16b(cols) + o16b(rows) + o16b(rowbytes) + o16b(flags))
    fp.write(o8(bpp))
    fp.write(o8(version))
    fp.write(o16b(offset))
    fp.write(o8(transparent_index))
    fp.write(o8(compression_type))
    fp.write(o16b(0))  # reserved by Palm

    # now write colormap if necessary

    if colormapsize:
        fp.write(o16b(colors))
        for i in range(colors):
            fp.write(o8(i))
            fp.write(colormap[3 * i : 3 * i + 3])

    # now convert data to raw form
    ImageFile._save(
        im, fp, [ImageFile._Tile("raw", (0, 0) + im.size, 0, (rawmode, rowbytes, 1))]
    )

    if hasattr(fp, "flush"):
        fp.flush()


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.width == 0 or im.height == 0:
        msg = "Cannot write empty image as PCX"
        raise ValueError(msg)

    try:
        version, bits, planes, rawmode = SAVE[im.mode]
    except KeyError as e:
        msg = f"Cannot save {im.mode} images as PCX"
        raise ValueError(msg) from e

    # bytes per plane
    stride = (im.size[0] * bits + 7) // 8
    # stride should be even
    stride += stride % 2
    # Stride needs to be kept in sync with the PcxEncode.c version.
    # Ideally it should be passed in in the state, but the bytes value
    # gets overwritten.

    logger.debug(
        "PcxImagePlugin._save: xwidth: %d, bits: %d, stride: %d",
        im.size[0],
        bits,
        stride,
    )

    # under windows, we could determine the current screen size with
    # "Image.core.display_mode()[1]", but I think that's overkill...

    screen = im.size

    dpi = 100, 100

    # PCX header
    fp.write(
        o8(10)
        + o8(version)
        + o8(1)
        + o8(bits)
        + o16(0)
        + o16(0)
        + o16(im.size[0] - 1)
        + o16(im.size[1] - 1)
        + o16(dpi[0])
        + o16(dpi[1])
        + b"\0" * 24
        + b"\xff" * 24
        + b"\0"
        + o8(planes)
        + o16(stride)
        + o16(1)
        + o16(screen[0])
        + o16(screen[1])
        + b"\0" * 54
    )

    assert fp.tell() == 128

    ImageFile._save(
        im, fp, [ImageFile._Tile("pcx", (0, 0) + im.size, 0, (rawmode, bits * planes))]
    )

    if im.mode == "P":
        # colour palette
        fp.write(o8(12))
        palette = im.im.getpalette("RGB", "RGB")
        palette += b"\x00" * (768 - len(palette))
        fp.write(palette)  # 768 bytes
    elif im.mode == "L":
        # grayscale palette
        fp.write(o8(12))
        for i in range(256):
            fp.write(o8(i) * 3)


def _save(
    im: Image.Image, fp: IO[bytes], filename: str | bytes, save_all: bool = False
) -> None:
    is_appending = im.encoderinfo.get("append", False)
    filename_str = filename.decode() if isinstance(filename, bytes) else filename
    if is_appending:
        existing_pdf = PdfParser.PdfParser(f=fp, filename=filename_str, mode="r+b")
    else:
        existing_pdf = PdfParser.PdfParser(f=fp, filename=filename_str, mode="w+b")

    dpi = im.encoderinfo.get("dpi")
    if dpi:
        x_resolution = dpi[0]
        y_resolution = dpi[1]
    else:
        x_resolution = y_resolution = im.encoderinfo.get("resolution", 72.0)

    info = {
        "title": (
            None if is_appending else os.path.splitext(os.path.basename(filename))[0]
        ),
        "author": None,
        "subject": None,
        "keywords": None,
        "creator": None,
        "producer": None,
        "creationDate": None if is_appending else time.gmtime(),
        "modDate": None if is_appending else time.gmtime(),
    }
    for k, default in info.items():
        v = im.encoderinfo.get(k) if k in im.encoderinfo else default
        if v:
            existing_pdf.info[k[0].upper() + k[1:]] = v

    #
    # make sure image data is available
    im.load()

    existing_pdf.start_writing()
    existing_pdf.write_header()
    existing_pdf.write_comment("created by Pillow PDF driver")

    #
    # pages
    ims = [im]
    if save_all:
        append_images = im.encoderinfo.get("append_images", [])
        for append_im in append_images:
            append_im.encoderinfo = im.encoderinfo.copy()
            ims.append(append_im)
    number_of_pages = 0
    image_refs = []
    page_refs = []
    contents_refs = []
    for im in ims:
        im_number_of_pages = 1
        if save_all:
            im_number_of_pages = getattr(im, "n_frames", 1)
        number_of_pages += im_number_of_pages
        for i in range(im_number_of_pages):
            image_refs.append(existing_pdf.next_object_id(0))
            if im.mode == "P" and "transparency" in im.info:
                image_refs.append(existing_pdf.next_object_id(0))

            page_refs.append(existing_pdf.next_object_id(0))
            contents_refs.append(existing_pdf.next_object_id(0))
            existing_pdf.pages.append(page_refs[-1])

    #
    # catalog and list of pages
    existing_pdf.write_catalog()

    page_number = 0
    for im_sequence in ims:
        im_pages: ImageSequence.Iterator | list[Image.Image] = (
            ImageSequence.Iterator(im_sequence) if save_all else [im_sequence]
        )
        for im in im_pages:
            image_ref, procset = _write_image(im, filename, existing_pdf, image_refs)

            #
            # page

            existing_pdf.write_page(
                page_refs[page_number],
                Resources=PdfParser.PdfDict(
                    ProcSet=[PdfParser.PdfName("PDF"), PdfParser.PdfName(procset)],
                    XObject=PdfParser.PdfDict(image=image_ref),
                ),
                MediaBox=[
                    0,
                    0,
                    im.width * 72.0 / x_resolution,
                    im.height * 72.0 / y_resolution,
                ],
                Contents=contents_refs[page_number],
            )

            #
            # page contents

            page_contents = b"q %f 0 0 %f 0 0 cm /image Do Q\n" % (
                im.width * 72.0 / x_resolution,
                im.height * 72.0 / y_resolution,
            )

            existing_pdf.write_obj(contents_refs[page_number], stream=page_contents)

            page_number += 1

    #
    # trailer
    existing_pdf.write_xref_and_trailer()
    if hasattr(fp, "flush"):
        fp.flush()
    existing_pdf.close()


def _save(
    im: Image.Image,
    fp: IO[bytes],
    filename: str | bytes,
    chunk: Callable[..., None] = putchunk,
    save_all: bool = False,
) -> None:
    # save an image to disk (called by the save method)

    if save_all:
        default_image = im.encoderinfo.get(
            "default_image", im.info.get("default_image")
        )
        modes = set()
        sizes = set()
        append_images = im.encoderinfo.get("append_images", [])
        for im_seq in itertools.chain([im], append_images):
            for im_frame in ImageSequence.Iterator(im_seq):
                modes.add(im_frame.mode)
                sizes.add(im_frame.size)
        for mode in ("RGBA", "RGB", "P"):
            if mode in modes:
                break
        else:
            mode = modes.pop()
        size = tuple(max(frame_size[i] for frame_size in sizes) for i in range(2))
    else:
        size = im.size
        mode = im.mode

    outmode = mode
    palette = []
    if im.palette:
        palette = im.getpalette() or []
    if mode == "P":
        #
        # attempt to minimize storage requirements for palette images
        if "bits" in im.encoderinfo:
            # number of bits specified by user
            colors = min(1 << im.encoderinfo["bits"], 256)
        else:
            # check palette contents
            if im.palette:
                colors = max(min(len(palette) // 3, 256), 1)
            else:
                colors = 256

        if colors <= 16:
            if colors <= 2:
                bits = 1
            elif colors <= 4:
                bits = 2
            else:
                bits = 4
            outmode += f";{bits}"

    # get the corresponding PNG mode
    try:
        rawmode, bit_depth, color_type = _OUTMODES[outmode]
    except KeyError as e:
        msg = f"cannot write mode {mode} as PNG"
        raise OSError(msg) from e
    if outmode == "I":
        deprecate("Saving I mode images as PNG", 13, stacklevel=4)

    #
    # write minimal PNG file

    fp.write(_MAGIC)

    chunk(
        fp,
        b"IHDR",
        o32(size[0]),  # 0: size
        o32(size[1]),
        bit_depth,
        color_type,
        b"\0",  # 10: compression
        b"\0",  # 11: filter category
        b"\0",  # 12: interlace flag
    )

    chunks = [b"cHRM", b"cICP", b"gAMA", b"sBIT", b"sRGB", b"tIME"]

    if icc := im.encoderinfo.get("icc_profile", im.info.get("icc_profile")):
        # ICC profile
        # according to PNG spec, the iCCP chunk contains:
        # Profile name  1-79 bytes (character string)
        # Null separator        1 byte (null character)
        # Compression method    1 byte (0)
        # Compressed profile    n bytes (zlib with deflate compression)
        name = b"ICC Profile"
        data = name + b"\0\0" + zlib.compress(icc)
        chunk(fp, b"iCCP", data)

        # You must either have sRGB or iCCP.
        # Disallow sRGB chunks when an iCCP-chunk has been emitted.
        chunks.remove(b"sRGB")

    if info := im.encoderinfo.get("pnginfo"):
        chunks_multiple_allowed = [b"sPLT", b"iTXt", b"tEXt", b"zTXt"]
        for info_chunk in info.chunks:
            cid, data = info_chunk[:2]
            if cid in chunks:
                chunks.remove(cid)
                chunk(fp, cid, data)
            elif cid in chunks_multiple_allowed:
                chunk(fp, cid, data)
            elif cid[1:2].islower():
                # Private chunk
                after_idat = len(info_chunk) == 3 and info_chunk[2]
                if not after_idat:
                    chunk(fp, cid, data)

    if im.mode == "P":
        palette_byte_number = colors * 3
        palette_bytes = bytes(palette[:palette_byte_number])
        while len(palette_bytes) < palette_byte_number:
            palette_bytes += b"\0"
        chunk(fp, b"PLTE", palette_bytes)

    transparency = im.encoderinfo.get("transparency", im.info.get("transparency"))

    if transparency is not None:
        if im.mode == "P":
            # limit to actual palette size
            alpha_bytes = colors
            if isinstance(transparency, bytes):
                chunk(fp, b"tRNS", transparency[:alpha_bytes])
            elif isinstance(transparency, int):
                transparency = max(0, min(255, transparency))
                alpha = b"\xff" * transparency + b"\0"
                chunk(fp, b"tRNS", alpha[:alpha_bytes])
            else:
                msg = "transparency for P must be an integer or bytes"
                raise ValueError(msg)
        elif im.mode in ("1", "L", "I", "I;16"):
            if isinstance(transparency, int):
                transparency = max(0, min(65535, transparency))
                chunk(fp, b"tRNS", o16(transparency))
            else:
                msg = f"transparency for {im.mode} must be an integer"
                raise ValueError(msg)
        elif im.mode == "RGB":
            if not isinstance(transparency, (list, tuple)):
                msg = "transparency for RGB must be list or tuple"
                raise ValueError(msg)
            elif len(transparency) != 3:
                msg = "transparency for RGB must have length 3"
                raise ValueError(msg)
            else:
                red, green, blue = transparency
                chunk(fp, b"tRNS", o16(red) + o16(green) + o16(blue))
        elif im.encoderinfo.get("transparency") is not None:
            # don't bother with transparency if it's an RGBA
            # and it's in the info dict. It's probably just stale.
            msg = "cannot use transparency for this mode"
            raise OSError(msg)
    elif im.mode == "P" and im.im.getpalettemode() == "RGBA":
        alpha = im.im.getpalette("RGBA", "A")
        alpha_bytes = colors
        chunk(fp, b"tRNS", alpha[:alpha_bytes])

    if dpi := im.encoderinfo.get("dpi"):
        chunk(
            fp,
            b"pHYs",
            o32(int(dpi[0] / 0.0254 + 0.5)),
            o32(int(dpi[1] / 0.0254 + 0.5)),
            b"\x01",
        )

    if info:
        chunks = [b"bKGD", b"hIST"]
        for info_chunk in info.chunks:
            cid, data = info_chunk[:2]
            if cid in chunks:
                chunks.remove(cid)
                chunk(fp, cid, data)

    if exif := im.encoderinfo.get("exif"):
        if isinstance(exif, Image.Exif):
            exif = exif.tobytes(8)
        if exif.startswith(b"Exif\x00\x00"):
            exif = exif[6:]
        chunk(fp, b"eXIf", exif)

    single_im: Image.Image | None = im
    if save_all:
        single_im = _write_multiple_frames(
            im, fp, chunk, mode, rawmode, default_image, append_images
        )
    if single_im:
        _apply_encoderinfo(single_im, im.encoderinfo)
        ImageFile._save(
            single_im,
            cast(IO[bytes], _idat(fp, chunk)),
            [ImageFile._Tile("zip", (0, 0) + single_im.size, 0, rawmode)],
        )

    if info:
        for info_chunk in info.chunks:
            cid, data = info_chunk[:2]
            if cid[1:2].islower():
                # Private chunk
                after_idat = len(info_chunk) == 3 and info_chunk[2]
                if after_idat:
                    chunk(fp, cid, data)

    chunk(fp, b"IEND", b"")

    if hasattr(fp, "flush"):
        fp.flush()


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode == "1":
        rawmode, head = "1;I", b"P4"
    elif im.mode == "L":
        rawmode, head = "L", b"P5"
    elif im.mode in ("I", "I;16"):
        rawmode, head = "I;16B", b"P5"
    elif im.mode in ("RGB", "RGBA"):
        rawmode, head = "RGB", b"P6"
    elif im.mode == "F":
        rawmode, head = "F;32F", b"Pf"
    else:
        msg = f"cannot write mode {im.mode} as PPM"
        raise OSError(msg)
    fp.write(head + b"\n%d %d\n" % im.size)
    if head == b"P6":
        fp.write(b"255\n")
    elif head == b"P5":
        if rawmode == "L":
            fp.write(b"255\n")
        else:
            fp.write(b"65535\n")
    elif head == b"Pf":
        fp.write(b"-1.0\n")
    row_order = -1 if im.mode == "F" else 1
    ImageFile._save(
        im, fp, [ImageFile._Tile("raw", (0, 0) + im.size, 0, (rawmode, 0, row_order))]
    )


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode == "RGB":
        channels = 3
    elif im.mode == "RGBA":
        channels = 4
    else:
        msg = "Unsupported QOI image mode"
        raise ValueError(msg)

    colorspace = 0 if im.encoderinfo.get("colorspace") == "sRGB" else 1

    fp.write(b"qoif")
    fp.write(o32(im.size[0]))
    fp.write(o32(im.size[1]))
    fp.write(o8(channels))
    fp.write(o8(colorspace))

    ImageFile._save(im, fp, [ImageFile._Tile("qoi", (0, 0) + im.size)])


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode not in {"RGB", "RGBA", "L"}:
        msg = "Unsupported SGI image mode"
        raise ValueError(msg)

    # Get the keyword arguments
    info = im.encoderinfo

    # Byte-per-pixel precision, 1 = 8bits per pixel
    bpc = info.get("bpc", 1)

    if bpc not in (1, 2):
        msg = "Unsupported number of bytes per pixel"
        raise ValueError(msg)

    # Flip the image, since the origin of SGI file is the bottom-left corner
    orientation = -1
    # Define the file as SGI File Format
    magic_number = 474
    # Run-Length Encoding Compression - Unsupported at this time
    rle = 0

    # X Dimension = width / Y Dimension = height
    x, y = im.size
    # Z Dimension: Number of channels
    z = len(im.mode)
    # Number of dimensions (x,y,z)
    if im.mode == "L":
        dimension = 1 if y == 1 else 2
    else:
        dimension = 3

    # Minimum Byte value
    pinmin = 0
    # Maximum Byte value (255 = 8bits per pixel)
    pinmax = 255
    # Image name (79 characters max, truncated below in write)
    img_name = os.path.splitext(os.path.basename(filename))[0]
    if isinstance(img_name, str):
        img_name = img_name.encode("ascii", "ignore")
    # Standard representation of pixel in the file
    colormap = 0
    fp.write(struct.pack(">h", magic_number))
    fp.write(o8(rle))
    fp.write(o8(bpc))
    fp.write(struct.pack(">H", dimension))
    fp.write(struct.pack(">H", x))
    fp.write(struct.pack(">H", y))
    fp.write(struct.pack(">H", z))
    fp.write(struct.pack(">l", pinmin))
    fp.write(struct.pack(">l", pinmax))
    fp.write(struct.pack("4s", b""))  # dummy
    fp.write(struct.pack("79s", img_name))  # truncates to 79 chars
    fp.write(struct.pack("s", b""))  # force null byte after img_name
    fp.write(struct.pack(">l", colormap))
    fp.write(struct.pack("404s", b""))  # dummy

    rawmode = "L"
    if bpc == 2:
        rawmode = "L;16B"

    for channel in im.split():
        fp.write(channel.tobytes("raw", rawmode, 0, orientation))

    if hasattr(fp, "flush"):
        fp.flush()


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode != "F":
        im = im.convert("F")

    hdr = makeSpiderHeader(im)
    if len(hdr) < 256:
        msg = "Error creating Spider header"
        raise OSError(msg)

    # write the SPIDER header
    fp.writelines(hdr)

    rawmode = "F;32NF"  # 32-bit native floating point
    ImageFile._save(im, fp, [ImageFile._Tile("raw", (0, 0) + im.size, 0, rawmode)])


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    try:
        rawmode, bits, colormaptype, imagetype = SAVE[im.mode]
    except KeyError as e:
        msg = f"cannot write mode {im.mode} as TGA"
        raise OSError(msg) from e

    if "rle" in im.encoderinfo:
        rle = im.encoderinfo["rle"]
    else:
        compression = im.encoderinfo.get("compression", im.info.get("compression"))
        rle = compression == "tga_rle"
    if rle:
        if im.mode == "1":
            msg = f"cannot write mode {im.mode} as TGA with run-length encoding"
            raise OSError(msg)

        imagetype += 8

    id_section = im.encoderinfo.get("id_section", im.info.get("id_section", ""))
    id_len = len(id_section)
    if id_len > 255:
        id_len = 255
        id_section = id_section[:255]
        warnings.warn("id_section has been trimmed to 255 characters")

    if colormaptype:
        palette = im.im.getpalette("RGB", "BGR")
        colormaplength, colormapentry = len(palette) // 3, 24
    else:
        colormaplength, colormapentry = 0, 0

    if im.mode in ("LA", "RGBA"):
        flags = 8
    else:
        flags = 0

    orientation = im.encoderinfo.get("orientation", im.info.get("orientation", -1))
    if orientation > 0:
        flags = flags | 0x20

    fp.write(
        o8(id_len)
        + o8(colormaptype)
        + o8(imagetype)
        + o16(0)  # colormapfirst
        + o16(colormaplength)
        + o8(colormapentry)
        + o16(0)
        + o16(0)
        + o16(im.size[0])
        + o16(im.size[1])
        + o8(bits)
        + o8(flags)
    )

    if id_section:
        fp.write(id_section)

    if colormaptype:
        fp.write(palette)

    if rle:
        ImageFile._save(
            im,
            fp,
            [ImageFile._Tile("tga_rle", (0, 0) + im.size, 0, (rawmode, orientation))],
        )
    else:
        ImageFile._save(
            im,
            fp,
            [ImageFile._Tile("raw", (0, 0) + im.size, 0, (rawmode, 0, orientation))],
        )

    # write targa version 2 footer
    fp.write(b"\000" * 8 + b"TRUEVISION-XFILE." + b"\000")


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    try:
        rawmode, prefix, photo, format, bits, extra = SAVE_INFO[im.mode]
    except KeyError as e:
        msg = f"cannot write mode {im.mode} as TIFF"
        raise OSError(msg) from e

    encoderinfo = im.encoderinfo
    encoderconfig = im.encoderconfig

    ifd = ImageFileDirectory_v2(prefix=prefix)
    if encoderinfo.get("big_tiff"):
        ifd._bigtiff = True

    try:
        compression = encoderinfo["compression"]
    except KeyError:
        compression = im.info.get("compression")
        if isinstance(compression, int):
            # compression value may be from BMP. Ignore it
            compression = None
    if compression is None:
        compression = "raw"
    elif compression == "tiff_jpeg":
        # OJPEG is obsolete, so use new-style JPEG compression instead
        compression = "jpeg"
    elif compression == "tiff_deflate":
        compression = "tiff_adobe_deflate"

    libtiff = WRITE_LIBTIFF or compression != "raw"

    # required for color libtiff images
    ifd[PLANAR_CONFIGURATION] = 1

    ifd[IMAGEWIDTH] = im.size[0]
    ifd[IMAGELENGTH] = im.size[1]

    # write any arbitrary tags passed in as an ImageFileDirectory
    if "tiffinfo" in encoderinfo:
        info = encoderinfo["tiffinfo"]
    elif "exif" in encoderinfo:
        info = encoderinfo["exif"]
        if isinstance(info, bytes):
            exif = Image.Exif()
            exif.load(info)
            info = exif
    else:
        info = {}
    logger.debug("Tiffinfo Keys: %s", list(info))
    if isinstance(info, ImageFileDirectory_v1):
        info = info.to_v2()
    for key in info:
        if isinstance(info, Image.Exif) and key in TiffTags.TAGS_V2_GROUPS:
            ifd[key] = info.get_ifd(key)
        else:
            ifd[key] = info.get(key)
        try:
            ifd.tagtype[key] = info.tagtype[key]
        except Exception:
            pass  # might not be an IFD. Might not have populated type

    legacy_ifd = {}
    if hasattr(im, "tag"):
        legacy_ifd = im.tag.to_v2()

    supplied_tags = {**legacy_ifd, **getattr(im, "tag_v2", {})}
    if supplied_tags.get(PLANAR_CONFIGURATION) == 2 and EXTRASAMPLES in supplied_tags:
        # If the image used separate component planes,
        # then EXTRASAMPLES should be ignored when saving contiguously
        if SAMPLESPERPIXEL in supplied_tags:
            supplied_tags[SAMPLESPERPIXEL] -= len(supplied_tags[EXTRASAMPLES])
        del supplied_tags[EXTRASAMPLES]
    for tag in (
        # IFD offset that may not be correct in the saved image
        EXIFIFD,
        # Determined by the image format and should not be copied from legacy_ifd.
        SAMPLEFORMAT,
    ):
        if tag in supplied_tags:
            del supplied_tags[tag]

    # additions written by Greg Couch, gregc@cgl.ucsf.edu
    # inspired by image-sig posting from Kevin Cazabon, kcazabon@home.com
    if hasattr(im, "tag_v2"):
        # preserve tags from original TIFF image file
        for key in (
            RESOLUTION_UNIT,
            X_RESOLUTION,
            Y_RESOLUTION,
            IPTC_NAA_CHUNK,
            PHOTOSHOP_CHUNK,
            XMP,
        ):
            if key in im.tag_v2:
                if key == IPTC_NAA_CHUNK and im.tag_v2.tagtype[key] not in (
                    TiffTags.BYTE,
                    TiffTags.UNDEFINED,
                ):
                    del supplied_tags[key]
                else:
                    ifd[key] = im.tag_v2[key]
                    ifd.tagtype[key] = im.tag_v2.tagtype[key]

    # preserve ICC profile (should also work when saving other formats
    # which support profiles as TIFF) -- 2008-06-06 Florian Hoech
    icc = encoderinfo.get("icc_profile", im.info.get("icc_profile"))
    if icc:
        ifd[ICCPROFILE] = icc

    for key, name in [
        (IMAGEDESCRIPTION, "description"),
        (X_RESOLUTION, "resolution"),
        (Y_RESOLUTION, "resolution"),
        (X_RESOLUTION, "x_resolution"),
        (Y_RESOLUTION, "y_resolution"),
        (RESOLUTION_UNIT, "resolution_unit"),
        (SOFTWARE, "software"),
        (DATE_TIME, "date_time"),
        (ARTIST, "artist"),
        (COPYRIGHT, "copyright"),
    ]:
        if name in encoderinfo:
            ifd[key] = encoderinfo[name]

    dpi = encoderinfo.get("dpi")
    if dpi:
        ifd[RESOLUTION_UNIT] = 2
        ifd[X_RESOLUTION] = dpi[0]
        ifd[Y_RESOLUTION] = dpi[1]

    if bits != (1,):
        ifd[BITSPERSAMPLE] = bits
        if len(bits) != 1:
            ifd[SAMPLESPERPIXEL] = len(bits)
    if extra is not None:
        ifd[EXTRASAMPLES] = extra
    if format != 1:
        ifd[SAMPLEFORMAT] = format

    if PHOTOMETRIC_INTERPRETATION not in ifd:
        ifd[PHOTOMETRIC_INTERPRETATION] = photo
    elif im.mode in ("1", "L") and ifd[PHOTOMETRIC_INTERPRETATION] == 0:
        if im.mode == "1":
            inverted_im = im.copy()
            px = inverted_im.load()
            if px is not None:
                for y in range(inverted_im.height):
                    for x in range(inverted_im.width):
                        px[x, y] = 0 if px[x, y] == 255 else 255
                im = inverted_im
        else:
            im = ImageOps.invert(im)

    if im.mode in ["P", "PA"]:
        lut = im.im.getpalette("RGB", "RGB;L")
        colormap = []
        colors = len(lut) // 3
        for i in range(3):
            colormap += [v * 256 for v in lut[colors * i : colors * (i + 1)]]
            colormap += [0] * (256 - colors)
        ifd[COLORMAP] = colormap
    # data orientation
    w, h = ifd[IMAGEWIDTH], ifd[IMAGELENGTH]
    stride = len(bits) * ((w * bits[0] + 7) // 8)
    if ROWSPERSTRIP not in ifd:
        # aim for given strip size (64 KB by default) when using libtiff writer
        if libtiff:
            im_strip_size = encoderinfo.get("strip_size", STRIP_SIZE)
            rows_per_strip = 1 if stride == 0 else min(im_strip_size // stride, h)
            # JPEG encoder expects multiple of 8 rows
            if compression == "jpeg":
                rows_per_strip = min(((rows_per_strip + 7) // 8) * 8, h)
        else:
            rows_per_strip = h
        if rows_per_strip == 0:
            rows_per_strip = 1
        ifd[ROWSPERSTRIP] = rows_per_strip
    strip_byte_counts = 1 if stride == 0 else stride * ifd[ROWSPERSTRIP]
    strips_per_image = (h + ifd[ROWSPERSTRIP] - 1) // ifd[ROWSPERSTRIP]
    if strip_byte_counts >= 2**16:
        ifd.tagtype[STRIPBYTECOUNTS] = TiffTags.LONG
    ifd[STRIPBYTECOUNTS] = (strip_byte_counts,) * (strips_per_image - 1) + (
        stride * h - strip_byte_counts * (strips_per_image - 1),
    )
    ifd[STRIPOFFSETS] = tuple(
        range(0, strip_byte_counts * strips_per_image, strip_byte_counts)
    )  # this is adjusted by IFD writer
    # no compression by default:
    ifd[COMPRESSION] = COMPRESSION_INFO_REV.get(compression, 1)

    if im.mode == "YCbCr":
        for tag, default_value in {
            YCBCRSUBSAMPLING: (1, 1),
            REFERENCEBLACKWHITE: (0, 255, 128, 255, 128, 255),
        }.items():
            ifd.setdefault(tag, default_value)

    blocklist = [TILEWIDTH, TILELENGTH, TILEOFFSETS, TILEBYTECOUNTS]
    if libtiff:
        if "quality" in encoderinfo:
            quality = encoderinfo["quality"]
            if not isinstance(quality, int) or quality < 0 or quality > 100:
                msg = "Invalid quality setting"
                raise ValueError(msg)
            if compression != "jpeg":
                msg = "quality setting only supported for 'jpeg' compression"
                raise ValueError(msg)
            ifd[JPEGQUALITY] = quality

        logger.debug("Saving using libtiff encoder")
        logger.debug("Items: %s", sorted(ifd.items()))
        _fp = 0
        if hasattr(fp, "fileno"):
            try:
                fp.seek(0)
                _fp = fp.fileno()
            except io.UnsupportedOperation:
                pass

        # optional types for non core tags
        types = {}
        # STRIPOFFSETS and STRIPBYTECOUNTS are added by the library
        # based on the data in the strip.
        # OSUBFILETYPE is deprecated.
        # The other tags expect arrays with a certain length (fixed or depending on
        # BITSPERSAMPLE, etc), passing arrays with a different length will result in
        # segfaults. Block these tags until we add extra validation.
        # SUBIFD may also cause a segfault.
        blocklist += [
            OSUBFILETYPE,
            REFERENCEBLACKWHITE,
            STRIPBYTECOUNTS,
            STRIPOFFSETS,
            TRANSFERFUNCTION,
            SUBIFD,
        ]

        # bits per sample is a single short in the tiff directory, not a list.
        atts: dict[int, Any] = {BITSPERSAMPLE: bits[0]}
        # Merge the ones that we have with (optional) more bits from
        # the original file, e.g x,y resolution so that we can
        # save(load('')) == original file.
        for tag, value in itertools.chain(ifd.items(), supplied_tags.items()):
            # Libtiff can only process certain core items without adding
            # them to the custom dictionary.
            # Custom items are supported for int, float, unicode, string and byte
            # values. Other types and tuples require a tagtype.
            if tag not in TiffTags.LIBTIFF_CORE:
                if tag in TiffTags.TAGS_V2_GROUPS:
                    types[tag] = TiffTags.LONG8
                elif tag in ifd.tagtype:
                    types[tag] = ifd.tagtype[tag]
                elif isinstance(value, (int, float, str, bytes)) or (
                    isinstance(value, tuple)
                    and all(isinstance(v, (int, float, IFDRational)) for v in value)
                ):
                    type = TiffTags.lookup(tag).type
                    if type:
                        types[tag] = type
            if tag not in atts and tag not in blocklist:
                if isinstance(value, str):
                    atts[tag] = value.encode("ascii", "replace") + b"\0"
                elif isinstance(value, IFDRational):
                    atts[tag] = float(value)
                else:
                    atts[tag] = value

        if SAMPLEFORMAT in atts and len(atts[SAMPLEFORMAT]) == 1:
            atts[SAMPLEFORMAT] = atts[SAMPLEFORMAT][0]

        logger.debug("Converted items: %s", sorted(atts.items()))

        # libtiff always expects the bytes in native order.
        # we're storing image byte order. So, if the rawmode
        # contains I;16, we need to convert from native to image
        # byte order.
        if im.mode in ("I;16", "I;16B", "I;16L"):
            rawmode = "I;16N"

        # Pass tags as sorted list so that the tags are set in a fixed order.
        # This is required by libtiff for some tags. For example, the JPEGQUALITY
        # pseudo tag requires that the COMPRESS tag was already set.
        tags = list(atts.items())
        tags.sort()
        a = (rawmode, compression, _fp, filename, tags, types)
        encoder = Image._getencoder(im.mode, "libtiff", a, encoderconfig)
        encoder.setimage(im.im, (0, 0) + im.size)
        while True:
            errcode, data = encoder.encode(ImageFile.MAXBLOCK)[1:]
            if not _fp:
                fp.write(data)
            if errcode:
                break
        if errcode < 0:
            msg = f"encoder error {errcode} when writing image file"
            raise OSError(msg)

    else:
        for tag in blocklist:
            del ifd[tag]
        offset = ifd.save(fp)

        ImageFile._save(
            im,
            fp,
            [ImageFile._Tile("raw", (0, 0) + im.size, offset, (rawmode, stride, 1))],
        )

    # -- helper for multi-page save --
    if "_debug_multipage" in encoderinfo:
        # just to access o32 and o16 (using correct byte order)
        setattr(im, "_debug_multipage", ifd)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    lossless = im.encoderinfo.get("lossless", False)
    quality = im.encoderinfo.get("quality", 80)
    alpha_quality = im.encoderinfo.get("alpha_quality", 100)
    icc_profile = im.encoderinfo.get("icc_profile") or ""
    exif = im.encoderinfo.get("exif", b"")
    if isinstance(exif, Image.Exif):
        exif = exif.tobytes()
    if exif.startswith(b"Exif\x00\x00"):
        exif = exif[6:]
    xmp = im.encoderinfo.get("xmp", "")
    method = im.encoderinfo.get("method", 4)
    exact = 1 if im.encoderinfo.get("exact") else 0

    im = _convert_frame(im)

    data = _webp.WebPEncode(
        im.getim(),
        lossless,
        float(quality),
        float(alpha_quality),
        icc_profile,
        method,
        exact,
        exif,
        xmp,
    )
    if data is None:
        msg = "cannot write file as WebP (encoder returned None)"
        raise OSError(msg)

    fp.write(data)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if _handler is None or not hasattr(_handler, "save"):
        msg = "WMF save handler not installed"
        raise OSError(msg)
    _handler.save(im, fp, filename)


def _save(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    if im.mode != "1":
        msg = f"cannot write mode {im.mode} as XBM"
        raise OSError(msg)

    fp.write(f"#define im_width {im.size[0]}\n".encode("ascii"))
    fp.write(f"#define im_height {im.size[1]}\n".encode("ascii"))

    hotspot = im.encoderinfo.get("hotspot")
    if hotspot:
        fp.write(f"#define im_x_hot {hotspot[0]}\n".encode("ascii"))
        fp.write(f"#define im_y_hot {hotspot[1]}\n".encode("ascii"))

    fp.write(b"static char im_bits[] = {\n")

    ImageFile._save(im, fp, [ImageFile._Tile("xbm", (0, 0) + im.size)])

    fp.write(b"};\n")


def _save(
    obj,
    zip_file,
    pickle_module,
    pickle_protocol,
    _disable_byteorder_record,
):
    serialized_storages: dict[str, torch.storage.UntypedStorage] = {}
    id_map: dict[int, str] = {}

    # Since loading storages that view the same data with different dtypes is
    # not supported, we need to keep track of the dtype associated with each
    # storage data_ptr and throw an error if the dtype is ever different.
    # TODO: This feature could be added in the future
    storage_dtypes: dict[int, torch.dtype] = {}

    def persistent_id(obj):
        # FIXME: the docs say that persistent_id should only return a string
        # but torch store returns tuples. This works only in the binary protocol
        # see
        # https://docs.python.org/2/library/pickle.html#pickling-and-unpickling-external-objects
        # https://github.com/python/cpython/blob/master/Lib/pickle.py#L527-L537
        if isinstance(obj, torch.storage.TypedStorage) or torch.is_storage(obj):
            if isinstance(obj, torch.storage.TypedStorage):
                # TODO: Once we decide to break serialization FC, this case
                # can be deleted
                storage = obj._untyped_storage
                storage_dtype = obj.dtype
                storage_type_str = obj._pickle_storage_type()
                storage_type = getattr(torch, storage_type_str)
                storage_numel = obj._size()

            else:
                storage = obj
                storage_dtype = torch.uint8
                storage_type = normalize_storage_type(type(obj))
                storage_numel = storage.nbytes()

            # If storage is allocated, ensure that any other saved storages
            # pointing to the same data all have the same dtype. If storage is
            # not allocated, don't perform this check
            if str(storage.device) != "meta" and storage.data_ptr() != 0:
                if storage.data_ptr() in storage_dtypes:
                    if storage_dtype != storage_dtypes[storage.data_ptr()]:
                        raise RuntimeError(
                            "Cannot save multiple tensors or storages that "
                            "view the same data as different types"
                        )
                else:
                    storage_dtypes[storage.data_ptr()] = storage_dtype

            storage_key = id_map.setdefault(storage._cdata, str(len(id_map)))
            if hasattr(obj, "_fake_device") and obj._fake_device is not None:
                location = str(obj._fake_device)
            else:
                location = location_tag(storage)
            serialized_storages[storage_key] = storage

            return ("storage", storage_type, storage_key, location, storage_numel)

        return None

    # Write the pickle data for `obj`
    data_buf = io.BytesIO()

    class PyTorchPickler(pickle_module.Pickler):  # type: ignore[name-defined]
        def persistent_id(self, obj):
            return persistent_id(obj)  # noqa: F821

    pickler = PyTorchPickler(data_buf, protocol=pickle_protocol)
    pickler.dump(obj)

    # The class def keeps the persistent_id closure alive, leaking memory.
    del persistent_id

    data_value = data_buf.getvalue()
    zip_file.write_record("data.pkl", data_value, len(data_value))
    # .format_version is used to track
    #     1. version 1 represents the order of storages being changed from
    #        lexicographical based on keys to numerically ordered based on keys
    #     2. version 2 represents including storage_alignment as a record
    #        within the zipfile
    zip_file.write_record(".format_version", "1", len("1"))
    storage_alignment = str(_get_storage_alignment())
    zip_file.write_record(
        ".storage_alignment", storage_alignment, len(storage_alignment)
    )

    # Write byte order marker
    if not _disable_byteorder_record:
        if sys.byteorder not in ["little", "big"]:
            raise ValueError("Unknown endianness type: " + sys.byteorder)

        zip_file.write_record("byteorder", sys.byteorder, len(sys.byteorder))

    # Write each tensor to a file named tensor/the_tensor_key in the zip archive
    for key in serialized_storages:
        name = f"data/{key}"
        storage = serialized_storages[key]
        num_bytes = storage.nbytes()
        global _serialization_tls
        if _serialization_tls.skip_data:
            zip_file.write_record_metadata(name, num_bytes)
        else:
            # given that we copy things around anyway, we might use storage.cpu()
            # this means to that to get tensors serialized, you need to implement
            # .cpu() on the underlying Storage
            if storage.device.type != "cpu":
                from torch.utils.serialization import config

                if (
                    config.save.use_pinned_memory_for_d2h
                    and (
                        acc := torch.accelerator.current_accelerator(
                            check_available=True
                        )
                    )
                    is not None
                    and acc.type == storage.device.type
                ):
                    new_storage = torch.empty(
                        num_bytes, dtype=torch.uint8, device="cpu", pin_memory=True
                    ).untyped_storage()
                    new_storage.copy_(storage)
                    torch.accelerator.current_stream(storage.device.index).synchronize()
                    storage = new_storage
                else:
                    storage = storage.cpu()
            # Now that it is on the CPU we can directly copy it into the zip file
            zip_file.write_record(name, storage, num_bytes)


def _save(data: PyTreeT, directory: str | PathLike[str], *,
          overwrite: bool = True, ts_specs: PyTreeT | None = None) -> None:
  sync_key = _get_unique_sync_key()  # get a synchronization key for multi-host

  if _is_remote_path(directory) and not pathlib.epath_installed:
    raise RuntimeError("For saving to remote URLs (e.g., gs, s3) you need the"
                       " `etils` module installed. You can install it using"
                       " `pip install etils`.")
  ts_specs = _tree_broadcast(ts_specs, data,
                             is_leaf=ts_impl.is_tensorstore_spec_leaf)
  data_flat, pytreedef = jax.tree.flatten(data, is_leaf=lambda x: x is None)
  if not all(x is None or _is_array_like(x) for x in data_flat):
    raise ValueError("For serialization, all leaves must be either None or"
                     " jax.Array-like objects.")
  distinct_locations = not _is_str_same_on_all_hosts(directory)
  if jax.process_count() > 1 and distinct_locations:
    raise ValueError(
        "Saving to different locations on different hosts is not supported,"
        " because it is extremely fragile. Consider using a single location.")
  root = _norm_path(directory)

  # 1. serialize the pytree #################################
  pytreedef_repr = utils.serialize_pytreedef(pytreedef)
  pytreedef_repr[utils._LEAF_IDS_KEY] = jax.tree.map(_leaf_to_desc, data_flat)

  pytreedef_repr = _prepare_directory(
      root, overwrite, pytreedef_repr, distinct_locations, sync_key)
  futures = []
  futures.append(_serialization_executor.submit(
      _write_pytreedef, root, pytreedef_repr, distinct_locations))

  # 2. serialize arrays #####################################
  array_store_path = root / _ARRAY_STORE_DIRNAME
  arrs = [data for data in data_flat if _is_array_like(data)]
  arr_leaf_ids = [i for i, data in enumerate(data_flat) if _is_array_like(data)]
  ts_specs_flat = jax.tree.leaves(ts_specs,
                                  is_leaf=ts_impl.is_tensorstore_spec_leaf)
  ts_specs_flat = [ts_specs_flat[i] for i in arr_leaf_ids]
  futures.append(_serialization_executor.submit(
      _write_arrays, array_store_path, arrs, arr_leaf_ids, ts_specs_flat,
      distinct_locations))

  # 3. wait for all futures to complete #####################
  _ = [fut.result() for fut in futures]
  _sync_on_key(sync_key, "array_serialization")

  # 4. finalize the array writing ###########################
  if len(arr_leaf_ids) > 0 and _USE_OCDBT:
    _serialization_executor.submit(  # call from a thread to not nest asyncio
        _finalize_array_store, array_store_path, distinct_locations).result()
  # we are done with all async ops here, we can block ####
  _sync_on_key(sync_key, "end")

