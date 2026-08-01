
def test_f2cmap(capfd, f2cmap_f90, monkeypatch):
    """Check that Fortran-to-Python KIND specs can be passed

    CLI :: --f2cmap
    """
    ipath = Path(f2cmap_f90)
    monkeypatch.setattr(sys, "argv", f'f2py -m blah {ipath} --f2cmap mapfile'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert "Reading f2cmap from 'mapfile' ..." in out
        assert "Mapping \"real(kind=real32)\" to \"float\"" in out
        assert "Mapping \"real(kind=real64)\" to \"double\"" in out
        assert "Mapping \"integer(kind=int64)\" to \"long_long\"" in out
        assert "Successfully applied user defined f2cmap changes" in out

