
def test_mod_gen_f77(capfd, hello_world_f90, monkeypatch):
    """Checks the generation of files based on a module name
    CLI :: -m
    """
    MNAME = "hi"
    foutl = get_io_paths(hello_world_f90, mname=MNAME)
    ipath = foutl.f90inp
    monkeypatch.setattr(sys, "argv", f'f2py {ipath} -m {MNAME}'.split())
    with util.switchdir(ipath.parent):
        f2pycli()

    # Always generate C module
    assert Path.exists(foutl.cmodf)
    # File contains a function, check for F77 wrappers
    assert Path.exists(foutl.wrap77)

