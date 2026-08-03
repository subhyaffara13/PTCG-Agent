import subprocess
import sys
from pathlib import Path


def test_npdistop(hello_world_f90, monkeypatch):
    """
    CLI :: -c
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(sys, "argv", f'f2py -m blah {ipath} -c'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        cmd_run = shlex.split(f"{sys.executable} -c \"import blah; blah.hi()\"")
        rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
        eout = ' Hello World\n'
        assert rout.stdout == eout

