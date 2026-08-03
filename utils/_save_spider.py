import os

def _save_spider(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    # get the filename extension and register it with Image
    if filename_ext := os.path.splitext(filename)[1]:
        ext = filename_ext.decode() if isinstance(filename_ext, bytes) else filename_ext
        Image.register_extension(SpiderImageFile.format, ext)
    _save(im, fp, filename)

