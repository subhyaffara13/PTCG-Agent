import sys

def test_version(capfd, monkeypatch):
    """Ensure version

    CLI :: -v
    """
    monkeypatch.setattr(sys, "argv", ["f2py", "-v"])
    # TODO: f2py2e should not call sys.exit() after printing the version
    with pytest.raises(SystemExit):
        f2pycli()
        out, _ = capfd.readouterr()
        import numpy as np
        assert np.__version__ == out.strip()

