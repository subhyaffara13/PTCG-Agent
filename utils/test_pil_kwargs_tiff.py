
def test_pil_kwargs_tiff():
    buf = io.BytesIO()
    pil_kwargs = {"description": "test image"}
    plt.figure().savefig(buf, format="tiff", pil_kwargs=pil_kwargs)
    im = Image.open(buf)
    tags = {TiffTags.TAGS_V2[k].name: v for k, v in im.tag_v2.items()}
    assert tags["ImageDescription"] == "test image"

