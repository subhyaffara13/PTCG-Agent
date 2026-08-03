from pathlib import Path


def test_find_ttc():
    fp = FontProperties(family=["WenQuanYi Zen Hei"])
    fontpath = findfont(fp)
    if Path(fontpath).name != "wqy-zenhei.ttc":
        pytest.skip("Font wqy-zenhei.ttc may be missing")
    # All fonts from this collection should have loaded as well.
    for name in ["WenQuanYi Zen Hei Mono", "WenQuanYi Zen Hei Sharp"]:
        subfontpath = findfont(FontProperties(family=[name]), fallback_to_default=False)
        assert subfontpath.path == fontpath.path
        assert subfontpath.face_index != fontpath.face_index
        subfont = get_font(subfontpath)
        assert subfont.fname == subfontpath.path
        assert subfont.face_index == subfontpath.face_index
    fig, ax = plt.subplots()
    ax.text(.5, .5, "\N{KANGXI RADICAL DRAGON}", fontproperties=fp)
    for fmt in ["raw", "svg", "pdf", "ps"]:
        fig.savefig(BytesIO(), format=fmt)

