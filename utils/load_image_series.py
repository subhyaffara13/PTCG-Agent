import os

def loadImageSeries(filelist: list[str] | None = None) -> list[Image.Image] | None:
    """create a list of :py:class:`~PIL.Image.Image` objects for use in a montage"""
    if filelist is None or len(filelist) < 1:
        return None

    byte_imgs = []
    for img in filelist:
        if not os.path.exists(img):
            print(f"unable to find {img}")
            continue
        try:
            with Image.open(img) as im:
                assert isinstance(im, SpiderImageFile)
                byte_im = im.convert2byte()
        except Exception:
            if not isSpiderImage(img):
                print(f"{img} is not a Spider image file")
            continue
        byte_im.info["filename"] = img
        byte_imgs.append(byte_im)
    return byte_imgs

