import sys
from pathlib import Path


def test_debugcapi(capfd, hello_world_f90, monkeypatch):
    """Ensures that debugging wrappers are written

    CLI :: --debug-capi
    """
    ipath = Path(hello_world_f90)
    mname = "blah"
    monkeypatch.setattr(sys, "argv",
                        f'f2py -m {mname} {ipath} --debug-capi'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        with Path(f"./{mname}module.c").open() as ocmod:
            assert r"#define DEBUGCFUNCS" in ocmod.read()

