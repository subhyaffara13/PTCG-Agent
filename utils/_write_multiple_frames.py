
def _write_multiple_frames(
    im: Image.Image, fp: IO[bytes], palette: _Palette | None
) -> bool:
    duration = im.encoderinfo.get("duration")
    disposal = im.encoderinfo.get("disposal", im.info.get("disposal"))

    im_frames: list[_Frame] = []
    previous_im: Image.Image | None = None
    frame_count = 0
    background_im = None
    for imSequence in itertools.chain([im], im.encoderinfo.get("append_images", [])):
        for im_frame in ImageSequence.Iterator(imSequence):
            # a copy is required here since seek can still mutate the image
            im_frame = _normalize_mode(im_frame.copy())
            if frame_count == 0:
                for k, v in im_frame.info.items():
                    if k == "transparency":
                        continue
                    if isinstance(k, str):
                        im.encoderinfo.setdefault(k, v)

            encoderinfo = im.encoderinfo.copy()
            if "transparency" in im_frame.info:
                encoderinfo.setdefault("transparency", im_frame.info["transparency"])
            im_frame = _normalize_palette(im_frame, palette, encoderinfo)
            if isinstance(duration, (list, tuple)):
                encoderinfo["duration"] = duration[frame_count]
            elif duration is None and "duration" in im_frame.info:
                encoderinfo["duration"] = im_frame.info["duration"]
            if isinstance(disposal, (list, tuple)):
                encoderinfo["disposal"] = disposal[frame_count]
            frame_count += 1

            diff_frame = None
            if im_frames and previous_im:
                # delta frame
                delta, bbox = _getbbox(previous_im, im_frame)
                if not bbox:
                    # This frame is identical to the previous frame
                    if encoderinfo.get("duration"):
                        im_frames[-1].encoderinfo["duration"] += encoderinfo["duration"]
                    continue
                if im_frames[-1].encoderinfo.get("disposal") == 2:
                    # To appear correctly in viewers using a convention,
                    # only consider transparency, and not background color
                    color = im.encoderinfo.get(
                        "transparency", im.info.get("transparency")
                    )
                    if color is not None:
                        if background_im is None:
                            background = _get_background(im_frame, color)
                            background_im = Image.new("P", im_frame.size, background)
                            first_palette = im_frames[0].im.palette
                            assert first_palette is not None
                            background_im.putpalette(first_palette, first_palette.mode)
                        bbox = _getbbox(background_im, im_frame)[1]
                    else:
                        bbox = (0, 0) + im_frame.size
                elif encoderinfo.get("optimize") and im_frame.mode != "1":
                    if "transparency" not in encoderinfo:
                        assert im_frame.palette is not None
                        try:
                            encoderinfo["transparency"] = (
                                im_frame.palette._new_color_index(im_frame)
                            )
                        except ValueError:
                            pass
                    if "transparency" in encoderinfo:
                        # When the delta is zero, fill the image with transparency
                        diff_frame = im_frame.copy()
                        fill = Image.new("P", delta.size, encoderinfo["transparency"])
                        if delta.mode == "RGBA":
                            r, g, b, a = delta.split()
                            mask = ImageMath.lambda_eval(
                                lambda args: args["convert"](
                                    args["max"](
                                        args["max"](
                                            args["max"](args["r"], args["g"]), args["b"]
                                        ),
                                        args["a"],
                                    )
                                    * 255,
                                    "1",
                                ),
                                r=r,
                                g=g,
                                b=b,
                                a=a,
                            )
                        else:
                            if delta.mode == "P":
                                # Convert to L without considering palette
                                delta_l = Image.new("L", delta.size)
                                delta_l.putdata(delta.get_flattened_data())
                                delta = delta_l
                            mask = ImageMath.lambda_eval(
                                lambda args: args["convert"](args["im"] * 255, "1"),
                                im=delta,
                            )
                        diff_frame.paste(fill, mask=ImageOps.invert(mask))
            else:
                bbox = None
            previous_im = im_frame
            im_frames.append(_Frame(diff_frame or im_frame, bbox, encoderinfo))

    if len(im_frames) == 1:
        if "duration" in im.encoderinfo:
            # Since multiple frames will not be written, use the combined duration
            im.encoderinfo["duration"] = im_frames[0].encoderinfo["duration"]
        return False

    for frame_data in im_frames:
        im_frame = frame_data.im
        if not frame_data.bbox:
            # global header
            for s in _get_global_header(im_frame, frame_data.encoderinfo):
                fp.write(s)
            offset = (0, 0)
        else:
            # compress difference
            if not palette:
                frame_data.encoderinfo["include_color_table"] = True

            if frame_data.bbox != (0, 0) + im_frame.size:
                im_frame = im_frame.crop(frame_data.bbox)
            offset = frame_data.bbox[:2]
        _write_frame_data(fp, im_frame, offset, frame_data.encoderinfo)
    return True


def _write_multiple_frames(
    im: Image.Image,
    fp: IO[bytes],
    chunk: Callable[..., None],
    mode: str,
    rawmode: str,
    default_image: Image.Image | None,
    append_images: list[Image.Image],
) -> Image.Image | None:
    duration = im.encoderinfo.get("duration")
    loop = im.encoderinfo.get("loop", im.info.get("loop", 0))
    disposal = im.encoderinfo.get("disposal", im.info.get("disposal", Disposal.OP_NONE))
    blend = im.encoderinfo.get("blend", im.info.get("blend", Blend.OP_SOURCE))

    if default_image:
        chain = itertools.chain(append_images)
    else:
        chain = itertools.chain([im], append_images)

    im_frames: list[_Frame] = []
    frame_count = 0
    for im_seq in chain:
        for im_frame in ImageSequence.Iterator(im_seq):
            if im_frame.mode == mode:
                im_frame = im_frame.copy()
            else:
                im_frame = im_frame.convert(mode)
            encoderinfo = im.encoderinfo.copy()
            if isinstance(duration, (list, tuple)):
                encoderinfo["duration"] = duration[frame_count]
            elif duration is None and "duration" in im_frame.info:
                encoderinfo["duration"] = im_frame.info["duration"]
            if isinstance(disposal, (list, tuple)):
                encoderinfo["disposal"] = disposal[frame_count]
            if isinstance(blend, (list, tuple)):
                encoderinfo["blend"] = blend[frame_count]
            frame_count += 1

            if im_frames:
                previous = im_frames[-1]
                prev_disposal = previous.encoderinfo.get("disposal")
                prev_blend = previous.encoderinfo.get("blend")
                if prev_disposal == Disposal.OP_PREVIOUS and len(im_frames) < 2:
                    prev_disposal = Disposal.OP_BACKGROUND

                if prev_disposal == Disposal.OP_BACKGROUND:
                    base_im = previous.im.copy()
                    dispose = Image.core.fill("RGBA", im.size, (0, 0, 0, 0))
                    bbox = previous.bbox
                    if bbox:
                        dispose = dispose.crop(bbox)
                    else:
                        bbox = (0, 0) + im.size
                    base_im.paste(dispose, bbox)
                elif prev_disposal == Disposal.OP_PREVIOUS:
                    base_im = im_frames[-2].im
                else:
                    base_im = previous.im
                delta = ImageChops.subtract_modulo(
                    im_frame.convert("RGBA"), base_im.convert("RGBA")
                )
                bbox = delta.getbbox(alpha_only=False)
                if (
                    not bbox
                    and prev_disposal == encoderinfo.get("disposal")
                    and prev_blend == encoderinfo.get("blend")
                    and "duration" in encoderinfo
                ):
                    previous.encoderinfo["duration"] += encoderinfo["duration"]
                    continue
            else:
                bbox = None
            im_frames.append(_Frame(im_frame, bbox, encoderinfo))

    if len(im_frames) == 1 and not default_image:
        return im_frames[0].im

    # animation control
    chunk(
        fp,
        b"acTL",
        o32(len(im_frames)),  # 0: num_frames
        o32(loop),  # 4: num_plays
    )

    # default image IDAT (if it exists)
    if default_image:
        default_im = im if im.mode == mode else im.convert(mode)
        _apply_encoderinfo(default_im, im.encoderinfo)
        ImageFile._save(
            default_im,
            cast(IO[bytes], _idat(fp, chunk)),
            [ImageFile._Tile("zip", (0, 0) + im.size, 0, rawmode)],
        )

    seq_num = 0
    for frame, frame_data in enumerate(im_frames):
        im_frame = frame_data.im
        if not frame_data.bbox:
            bbox = (0, 0) + im_frame.size
        else:
            bbox = frame_data.bbox
            im_frame = im_frame.crop(bbox)
        size = im_frame.size
        encoderinfo = frame_data.encoderinfo
        frame_duration = encoderinfo.get("duration", 0)
        delay = Fraction(frame_duration / 1000).limit_denominator(65535)
        if delay.numerator > 65535:
            msg = "cannot write duration"
            raise ValueError(msg)
        frame_disposal = encoderinfo.get("disposal", disposal)
        frame_blend = encoderinfo.get("blend", blend)
        # frame control
        chunk(
            fp,
            b"fcTL",
            o32(seq_num),  # sequence_number
            o32(size[0]),  # width
            o32(size[1]),  # height
            o32(bbox[0]),  # x_offset
            o32(bbox[1]),  # y_offset
            o16(delay.numerator),  # delay_numerator
            o16(delay.denominator),  # delay_denominator
            o8(frame_disposal),  # dispose_op
            o8(frame_blend),  # blend_op
        )
        seq_num += 1
        # frame data
        _apply_encoderinfo(im_frame, im.encoderinfo)
        if frame == 0 and not default_image:
            # first frame must be in IDAT chunks for backwards compatibility
            ImageFile._save(
                im_frame,
                cast(IO[bytes], _idat(fp, chunk)),
                [ImageFile._Tile("zip", (0, 0) + im_frame.size, 0, rawmode)],
            )
        else:
            fdat_chunks = _fdat(fp, chunk, seq_num)
            ImageFile._save(
                im_frame,
                cast(IO[bytes], fdat_chunks),
                [ImageFile._Tile("zip", (0, 0) + im_frame.size, 0, rawmode)],
            )
            seq_num = fdat_chunks.seq_num
    return None

