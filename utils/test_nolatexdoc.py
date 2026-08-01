
def test_nolatexdoc(capfd, hello_world_f90, monkeypatch):
    """Ensures that TeX documentation is written out

    CLI :: --no-latex-doc
    """
    ipath = Path(hello_world_f90)
    mname = "blah"
    monkeypatch.setattr(sys, "argv",
                        f'f2py -m {mname} {ipath} --no-latex-doc'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert "Documentation is saved to file" not in out

