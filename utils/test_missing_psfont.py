
def test_missing_psfont(fmt, monkeypatch):
    """An error is raised if a TeX font lacks a Type-1 equivalent"""
    monkeypatch.setattr(
        dviread.PsfontsMap, '__getitem__',
        lambda self, k: dviread.PsFont(
            texname=b'texfont', psname=b'Some Font',
            effects=None, encoding=None, filename=None))
    mpl.rcParams['text.usetex'] = True
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, 'hello')
    with TemporaryFile() as tmpfile, pytest.raises(ValueError):
        fig.savefig(tmpfile, format=fmt)

