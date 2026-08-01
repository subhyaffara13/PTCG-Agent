
def test_find_noto():
    fp = FontProperties(family=["Noto Sans CJK SC", "Noto Sans CJK JP"])
    name = Path(findfont(fp)).name
    if name not in ("NotoSansCJKsc-Regular.otf", "NotoSansCJK-Regular.ttc"):
        pytest.skip(f"Noto Sans CJK SC font may be missing (found {name})")

    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, 'Hello, 你好', fontproperties=fp)
    for fmt in ["raw", "svg", "pdf", "ps"]:
        fig.savefig(BytesIO(), format=fmt)

