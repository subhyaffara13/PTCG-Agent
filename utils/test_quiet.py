
def test_quiet(capfd, hello_world_f90, monkeypatch):
    """Reduce verbosity

    CLI :: --quiet
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(sys, "argv", f'f2py -m blah {ipath} --quiet'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert len(out) == 0

