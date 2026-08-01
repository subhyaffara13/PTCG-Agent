
def test_wrapfunc_def(capfd, hello_world_f90, monkeypatch):
    """Ensures that fortran subroutine wrappers for F77 are included by default

    CLI :: --[no]-wrap-functions
    """
    # Implied
    ipath = Path(hello_world_f90)
    mname = "blah"
    monkeypatch.setattr(sys, "argv", f'f2py -m {mname} {ipath}'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
    out, _ = capfd.readouterr()
    assert r"Fortran 77 wrappers are saved to" in out

    # Explicit
    monkeypatch.setattr(sys, "argv",
                        f'f2py -m {mname} {ipath} --wrap-functions'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert r"Fortran 77 wrappers are saved to" in out

