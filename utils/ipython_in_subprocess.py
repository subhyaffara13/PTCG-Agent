
def ipython_in_subprocess(requested_backend_or_gui_framework, all_expected_backends):
    import pytest
    IPython = pytest.importorskip("IPython")

    if sys.platform == "win32":
        pytest.skip("Cannot change backend running IPython in subprocess on Windows")

    if (IPython.version_info[:3] == (8, 24, 0) and
            requested_backend_or_gui_framework == "osx"):
        pytest.skip("Bug using macosx backend in IPython 8.24.0 fixed in 8.24.1")

    # This code can be removed when Python 3.12, the latest version supported
    # by IPython < 8.24, reaches end-of-life in late 2028.
    for min_version, backend in all_expected_backends.items():
        if IPython.version_info[:2] >= min_version:
            expected_backend = backend
            break

    code = ("import matplotlib as mpl, matplotlib.pyplot as plt;"
            "fig, ax=plt.subplots(); ax.plot([1, 3, 2]); mpl.get_backend()")
    proc = subprocess_run_for_testing(
        [
            "ipython",
            "--no-simple-prompt",
            f"--matplotlib={requested_backend_or_gui_framework}",
            "-c", code,
        ],
        check=True,
        capture_output=True,
    )

    assert proc.stdout.strip().endswith(f"'{expected_backend}'")

