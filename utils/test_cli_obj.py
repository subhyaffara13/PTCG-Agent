
def test_cli_obj(capfd, hello_world_f90, monkeypatch):
    """Ensures that the extra object can be specified when using meson backend
    """
    ipath = Path(hello_world_f90)
    mname = "blah"
    odir = "tttmp"
    obj = "extra.o"
    monkeypatch.setattr(sys, "argv",
                        f'f2py --backend meson --build-dir {odir} -m {mname} -c {obj} {ipath}'.split())

    with util.switchdir(ipath.parent):
        Path(obj).touch()
        compiler_check_f2pycli()
        with Path(f"{odir}/meson.build").open() as mesonbuild:
            mbld = mesonbuild.read()
            assert "objects:" in mbld
            assert f"'''{obj}'''" in mbld

