import sys
from pathlib import Path


def test_gh22819_many_pyf(capfd, gh22819_cli, monkeypatch):
    """Only one .pyf file allowed
    gh-22819
    CLI :: .pyf files
    """
    ipath = Path(gh22819_cli)
    monkeypatch.setattr(sys, "argv", f"f2py -m blah {ipath} hello.pyf".split())
    with util.switchdir(ipath.parent):
        with pytest.raises(ValueError, match="Only one .pyf file per call"):
            f2pycli()

