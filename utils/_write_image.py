
def _write_image(
    im: Image.Image,
    filename: str | bytes,
    existing_pdf: PdfParser.PdfParser,
    image_refs: list[PdfParser.IndirectReference],
) -> tuple[PdfParser.IndirectReference, str]:
    # FIXME: Should replace ASCIIHexDecode with RunLengthDecode
    # (packbits) or LZWDecode (tiff/lzw compression).  Note that
    # PDF 1.2 also supports Flatedecode (zip compression).

    params = None
    decode = None

    #
    # Get image characteristics

    width, height = im.size

    dict_obj: dict[str, Any] = {"BitsPerComponent": 8}
    if im.mode == "1":
        if features.check("libtiff"):
            decode_filter = "CCITTFaxDecode"
            dict_obj["BitsPerComponent"] = 1
            params = PdfParser.PdfArray(
                [
                    PdfParser.PdfDict(
                        {
                            "K": -1,
                            "BlackIs1": True,
                            "Columns": width,
                            "Rows": height,
                        }
                    )
                ]
            )
        else:
            decode_filter = "DCTDecode"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceGray")
        procset = "ImageB"  # grayscale
    elif im.mode == "L":
        decode_filter = "DCTDecode"
        # params = f"<< /Predictor 15 /Columns {width-2} >>"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceGray")
        procset = "ImageB"  # grayscale
    elif im.mode == "LA":
        decode_filter = "JPXDecode"
        # params = f"<< /Predictor 15 /Columns {width-2} >>"
        procset = "ImageB"  # grayscale
        dict_obj["SMaskInData"] = 1
    elif im.mode == "P":
        decode_filter = "ASCIIHexDecode"
        palette = im.getpalette()
        assert palette is not None
        dict_obj["ColorSpace"] = [
            PdfParser.PdfName("Indexed"),
            PdfParser.PdfName("DeviceRGB"),
            len(palette) // 3 - 1,
            PdfParser.PdfBinary(palette),
        ]
        procset = "ImageI"  # indexed color

        if "transparency" in im.info:
            smask = im.convert("LA").getchannel("A")
            smask.encoderinfo = {}

            image_ref = _write_image(smask, filename, existing_pdf, image_refs)[0]
            dict_obj["SMask"] = image_ref
    elif im.mode == "RGB":
        decode_filter = "DCTDecode"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceRGB")
        procset = "ImageC"  # color images
    elif im.mode == "RGBA":
        decode_filter = "JPXDecode"
        procset = "ImageC"  # color images
        dict_obj["SMaskInData"] = 1
    elif im.mode == "CMYK":
        decode_filter = "DCTDecode"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceCMYK")
        procset = "ImageC"  # color images
        decode = [1, 0, 1, 0, 1, 0, 1, 0]
    else:
        msg = f"cannot save mode {im.mode}"
        raise ValueError(msg)

    #
    # image

    op = io.BytesIO()

    if decode_filter == "ASCIIHexDecode":
        ImageFile._save(im, op, [ImageFile._Tile("hex", (0, 0) + im.size, 0, im.mode)])
    elif decode_filter == "CCITTFaxDecode":
        im.save(
            op,
            "TIFF",
            compression="group4",
            # use a single strip
            strip_size=math.ceil(width / 8) * height,
        )
    elif decode_filter == "DCTDecode":
        from . import JpegImagePlugin

        JpegImagePlugin._save(im, op, filename)
    elif decode_filter == "JPXDecode":
        from . import Jpeg2KImagePlugin

        del dict_obj["BitsPerComponent"]
        Jpeg2KImagePlugin._save(im, op, filename)
    else:
        msg = f"unsupported PDF filter ({decode_filter})"
        raise ValueError(msg)

    stream = op.getvalue()
    filter: PdfParser.PdfArray | PdfParser.PdfName
    if decode_filter == "CCITTFaxDecode":
        stream = stream[8:]
        filter = PdfParser.PdfArray([PdfParser.PdfName(decode_filter)])
    else:
        filter = PdfParser.PdfName(decode_filter)

    image_ref = image_refs.pop(0)
    existing_pdf.write_obj(
        image_ref,
        stream=stream,
        Type=PdfParser.PdfName("XObject"),
        Subtype=PdfParser.PdfName("Image"),
        Width=width,  # * 72.0 / x_resolution,
        Height=height,  # * 72.0 / y_resolution,
        Filter=filter,
        Decode=decode,
        DecodeParms=params,
        **dict_obj,
    )

    return image_ref, procset


def _writeImage(glyphObject: Any, element: ElementType, validate: bool) -> None:
    image = getattr(glyphObject, "image", None)
    if image is None:
        return

    if validate and not imageValidator(image):
        raise GlifLibError(
            "image attribute must be a dict or dict-like object with the proper structure."
        )
    attrs = OrderedDict([("fileName", image["fileName"])])
    for attr, default in _transformationInfo:
        value = image.get(attr, default)
        if value != default:
            attrs[attr] = repr(value)
    color = image.get("color")
    if color is not None:
        attrs["color"] = color
    etree.SubElement(element, "image", attrs)

