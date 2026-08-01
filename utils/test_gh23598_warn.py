
def test_gh23598_warn(capfd, gh23598_warn, monkeypatch):
    foutl = get_io_paths(gh23598_warn, mname="test")
    ipath = foutl.f90inp
    monkeypatch.setattr(
        sys, "argv",
        f'f2py {ipath} -m test'.split())

    with util.switchdir(ipath.parent):
        f2pycli()  # Generate files
        wrapper = foutl.wrap90.read_text()
        assert "intproductf2pywrap, intpr" not in wrapper

