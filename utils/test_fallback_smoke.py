
def test_fallback_smoke(fmt):
    fonts, test_str = _gen_multi_font_text()
    plt.rcParams['font.size'] = 16
    fig = plt.figure(figsize=(4.75, 1.85))
    fig.text(0.5, 0.5, test_str,
             horizontalalignment='center', verticalalignment='center')

    fig.savefig(io.BytesIO(), format=fmt)

