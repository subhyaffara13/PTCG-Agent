
def test_configdir_uses_localappdata_on_windows(tmp_path):
    """Test that on Windows, config/cache dir uses LOCALAPPDATA for fresh installs."""
    localappdata = tmp_path / "AppData/Local"
    localappdata.mkdir(parents=True)
    # Set USERPROFILE to tmp_path so the old location check finds nothing
    fake_home = tmp_path / "home"
    fake_home.mkdir()

    proc = subprocess_run_for_testing(
        [sys.executable, "-c",
         "import matplotlib; print(matplotlib.get_configdir())"],
        env={**os.environ, "LOCALAPPDATA": str(localappdata),
             "USERPROFILE": str(fake_home), "MPLCONFIGDIR": ""},
        capture_output=True, text=True, check=True)

    configdir = proc.stdout.strip()
    # On Windows with no existing old config, should use LOCALAPPDATA\matplotlib
    assert configdir == str(localappdata / "matplotlib")

