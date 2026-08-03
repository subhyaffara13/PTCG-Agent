import os
import sys

def test_configdir_uses_userprofile_on_windows_if_exists(tmp_path):
    """
    Test that on Windows, config/cache dir uses %USERPROFILE% if .matplotlib
    exists.
    """
    localappdata = tmp_path / "AppData/Local"
    localappdata.mkdir(parents=True)
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    old_configdir = fake_home / ".matplotlib"
    old_configdir.mkdir()

    proc = subprocess_run_for_testing(
        [sys.executable, "-c",
         "import matplotlib; print(matplotlib.get_configdir())"],
        env={**os.environ, "LOCALAPPDATA": str(localappdata),
             "USERPROFILE": str(fake_home), "MPLCONFIGDIR": ""},
        capture_output=True, text=True, check=True)

    configdir = proc.stdout.strip()
    # On Windows with existing old config, should continue using it
    assert configdir == str(old_configdir)

