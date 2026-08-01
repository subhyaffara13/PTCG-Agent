
def test_untitled_cli(capfd, hello_world_f90, monkeypatch):
    """Check that modules are named correctly

    CLI :: defaults
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(sys, "argv", f"f2py --backend meson -c {ipath}".split())
    with util.switchdir(ipath.parent):
        compiler_check_f2pycli()
        out, _ = capfd.readouterr()
        assert "untitledmodule.c" in out

