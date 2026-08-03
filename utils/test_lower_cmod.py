import re
import sys

def test_lower_cmod(capfd, hello_world_f77, monkeypatch):
    """Lowers cases by flag or when -h is present

    CLI :: --[no-]lower
    """
    foutl = get_io_paths(hello_world_f77, mname="test")
    ipath = foutl.finp
    capshi = re.compile(r"HI\(\)")
    capslo = re.compile(r"hi\(\)")
    # Case I: --lower is passed
    monkeypatch.setattr(sys, "argv", f'f2py {ipath} -m test --lower'.split())
    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert capslo.search(out) is not None
        assert capshi.search(out) is None
    # Case II: --no-lower is passed
    monkeypatch.setattr(sys, "argv",
                        f'f2py {ipath} -m test --no-lower'.split())
    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert capslo.search(out) is None
        assert capshi.search(out) is not None

