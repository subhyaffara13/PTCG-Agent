
def test_imsave_pil_kwargs_png():
    from PIL.PngImagePlugin import PngInfo
    buf = io.BytesIO()
    pnginfo = PngInfo()
    pnginfo.add_text("Software", "test")
    plt.imsave(buf, [[0, 1], [2, 3]],
               format="png", pil_kwargs={"pnginfo": pnginfo})
    im = Image.open(buf)
    assert im.info["Software"] == "test"

