
def test_afm_kerning():
    fn = fm.findfont("Helvetica", fontext="afm")
    with open(fn, 'rb') as fh:
        afm = _afm.AFM(fh)
    assert afm.get_kern_dist_from_name('A', 'V') == -70.0
    assert afm.get_kern_dist_from_name('V', 'A') == -80.0

