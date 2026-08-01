
def jpeg_factory(
    fp: IO[bytes], filename: str | bytes | None = None
) -> JpegImageFile | MpoImageFile:
    im = JpegImageFile(fp, filename)
    try:
        mpheader = im._getmp()
        if mpheader is not None and mpheader[45057] > 1:
            for segment, content in im.applist:
                if segment == "APP1" and b' hdrgm:Version="' in content:
                    # Ultra HDR images are not yet supported
                    return im
            # It's actually an MPO
            from .MpoImagePlugin import MpoImageFile

            # Don't reload everything, just convert it.
            im = MpoImageFile.adopt(im, mpheader)
    except (TypeError, IndexError):
        # It is really a JPEG
        pass
    except SyntaxError:
        warnings.warn(
            "Image appears to be a malformed MPO file, it will be "
            "interpreted as a base JPEG file"
        )
    return im

