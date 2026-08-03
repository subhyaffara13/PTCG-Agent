import re
from pathlib import Path


def test_font_selection(rc, preamble, family):
    plt.rcParams.update(rc)
    tm = TexManager()
    src = Path(tm.make_tex("hello, world", fontsize=12)).read_text()
    assert preamble in src
    assert [*re.findall(r"\\\w+family", src)] == [family]

