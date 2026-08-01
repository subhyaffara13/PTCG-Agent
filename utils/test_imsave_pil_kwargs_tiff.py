
def test_imsave_pil_kwargs_tiff():
    from PIL.TiffTags import TAGS_V2 as TAGS
    buf = io.BytesIO()
    pil_kwargs = {"description": "test image"}
    plt.imsave(buf, [[0, 1], [2, 3]], format="tiff", pil_kwargs=pil_kwargs)
    assert len(pil_kwargs) == 1
    im = Image.open(buf)
    tags = {TAGS[k].name: v for k, v in im.tag_v2.items()}
    assert tags["ImageDescription"] == "test image"

