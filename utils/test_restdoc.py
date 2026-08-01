
def test_restdoc(capfd, hello_world_f90, monkeypatch):
    """Ensures that RsT documentation is written out

    CLI :: --rest-doc
    """
    ipath = Path(hello_world_f90)
    mname = "blah"
    monkeypatch.setattr(sys, "argv",
                        f'f2py -m {mname} {ipath} --rest-doc'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert "ReST Documentation is saved to file" in out
        with Path(f"./{mname}module.rest").open() as orst:
            assert r".. -*- rest -*-" in orst.read()

