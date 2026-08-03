from typing import Any

def _write_frame_data(
    fp: IO[bytes],
    im_frame: Image.Image,
    offset: tuple[int, int],
    params: dict[str, Any],
) -> None:
    try:
        im_frame.encoderinfo = params

        # local image header
        _write_local_header(fp, im_frame, offset, 0)

        ImageFile._save(
            im_frame,
            fp,
            [ImageFile._Tile("gif", (0, 0) + im_frame.size, 0, RAWMODE[im_frame.mode])],
        )

        fp.write(b"\0")  # end of image data
    finally:
        del im_frame.encoderinfo

