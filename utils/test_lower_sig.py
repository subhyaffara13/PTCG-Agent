import re
import sys

def test_lower_sig(capfd, hello_world_f77, monkeypatch):
    """Lowers cases in signature files by flag or when -h is present

    CLI :: --[no-]lower -h
    """
    foutl = get_io_paths(hello_world_f77, mname="test")
    ipath = foutl.finp
    # Signature files
    capshi = re.compile(r"Block: HI")
    capslo = re.compile(r"Block: hi")
    # Case I: --lower is implied by -h
    # TODO: Clean up to prevent passing --overwrite-signature
    monkeypatch.setattr(
        sys,
        "argv",
        f'f2py {ipath} -h {foutl.pyf} -m test --overwrite-signature'.split(),
    )

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert capslo.search(out) is not None
        assert capshi.search(out) is None

    # Case II: --no-lower overrides -h
    monkeypatch.setattr(
        sys,
        "argv",
        f'f2py {ipath} -h {foutl.pyf} -m test --overwrite-signature --no-lower'
        .split(),
    )

    with util.switchdir(ipath.parent):
        f2pycli()
        out, _ = capfd.readouterr()
        assert capslo.search(out) is None
        assert capshi.search(out) is not None

