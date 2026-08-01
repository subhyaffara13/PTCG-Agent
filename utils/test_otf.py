
def test_otf():
    fname = '/usr/share/fonts/opentype/freefont/FreeMono.otf'
    if Path(fname).exists():
        with pytest.warns(mpl.MatplotlibDeprecationWarning):
            assert is_opentype_cff_font(fname)
    for f in fontManager.ttflist:
        if 'otf' in f.fname:
            with open(f.fname, 'rb') as fd:
                res = fd.read(4) == b'OTTO'
            with pytest.warns(mpl.MatplotlibDeprecationWarning):
                assert res == is_opentype_cff_font(f.fname)

