import re

def test_fonttype(fonttype):
    mpl.rcParams["ps.fonttype"] = fonttype
    fig, ax = plt.subplots()

    ax.text(0.25, 0.5, "Forty-two is the answer to everything!")

    buf = io.BytesIO()
    fig.savefig(buf, format="ps")

    test = b'/FontType ' + bytes(f"{fonttype}", encoding='utf-8') + b' def'

    assert re.search(test, buf.getvalue(), re.MULTILINE)

