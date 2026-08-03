import os
import subprocess
import sys
from pathlib import Path


def test_freethreading_compatible(hello_world_f90, monkeypatch):
    """
    CLI :: --freethreading_compatible
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(sys, "argv", f'f2py -m blah {ipath} -c --freethreading-compatible'.split())

    with util.switchdir(ipath.parent):
        compiler_check_f2pycli()
        cmd = f"{sys.executable} -c \"import blah; blah.hi();"
        if NOGIL_BUILD:
            cmd += "import sys; assert sys._is_gil_enabled() is False\""
        else:
            cmd += "\""
        cmd_run = shlex.split(cmd)
        rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
        eout = ' Hello World\n'
        assert rout.stdout == eout
        if "LSAN_OPTIONS" not in os.environ:
            assert rout.stderr == ""
        assert rout.returncode == 0

