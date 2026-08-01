
def test_backend_fallback_headful(tmp_path):
    if parse_version(pytest.__version__) >= parse_version('8.2.0'):
        pytest_kwargs = dict(exc_type=ImportError)
    else:
        pytest_kwargs = {}

    pytest.importorskip("tkinter", **pytest_kwargs)
    env = {**os.environ, "MPLBACKEND": "", "MPLCONFIGDIR": str(tmp_path)}
    backend = subprocess_run_for_testing(
        [sys.executable, "-c",
         "import matplotlib as mpl; "
         "sentinel = mpl.rcsetup._auto_backend_sentinel; "
         # Check that access on another instance does not resolve the sentinel.
         "assert mpl.RcParams({'backend': sentinel})['backend'] == sentinel; "
         "assert mpl.rcParams._get('backend') == sentinel; "
         "assert mpl.get_backend(auto_select=False) is None; "
         "import matplotlib.pyplot; "
         "print(matplotlib.get_backend())"],
        env=env, text=True, check=True, capture_output=True).stdout
    # The actual backend will depend on what's installed, but at least tkagg is
    # present.
    assert backend.strip().lower() != "agg"

