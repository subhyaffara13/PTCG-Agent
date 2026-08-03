import os
import subprocess
import sys

def test_tmpconfigdir_warning(tmp_path):
    """Test that a warning is emitted if a temporary configdir must be used."""
    mode = os.stat(tmp_path).st_mode
    try:
        os.chmod(tmp_path, 0)
        proc = subprocess_run_for_testing(
            [sys.executable, "-c", "import matplotlib"],
            env={**os.environ, "MPLCONFIGDIR": str(tmp_path)},
            stderr=subprocess.PIPE, text=True, check=True)
        assert "set the MPLCONFIGDIR" in proc.stderr
    finally:
        os.chmod(tmp_path, mode)

