import sys

def test_no_distutils_backend(capfd, hello_world_f90, monkeypatch):
    """Check that distutils backend and related options fail
    CLI :: --fcompiler --help-link --backend distutils
    """
    MNAME = "hi"
    foutl = get_io_paths(hello_world_f90, mname=MNAME)
    ipath = foutl.f90inp
    monkeypatch.setattr(
        sys, "argv", f"f2py {ipath} -c --fcompiler=gfortran -m {MNAME}".split()
    )
    with util.switchdir(ipath.parent):
        compiler_check_f2pycli()
        out, _ = capfd.readouterr()
        assert "--fcompiler cannot be used with meson" in out

    monkeypatch.setattr(
        sys, "argv", ["f2py", "--help-link"]
    )
    with pytest.raises(SystemExit):
        f2pycli()
        out, _ = capfd.readouterr()
        assert "Unknown option --help-link" in out

    monkeypatch.setattr(
        sys, "argv", ["f2py", "--backend", "distutils"]
    )
    with pytest.raises(SystemExit):
        compiler_check_f2pycli()
        f2pycli()
        out, _ = capfd.readouterr()
        assert "'distutils' backend was removed" in out

