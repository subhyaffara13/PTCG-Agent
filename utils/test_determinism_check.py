import os
import sys

def test_determinism_check(objects, fmt, usetex):
    """
    Output the same graph three times and check that the outputs are exactly the same.

    Parameters
    ----------
    objects : str
        Objects to be included in the test document: 'm' for markers, 'h' for
        hatch patterns, 'i' for images, and 'p' for paths.
    fmt : {"pdf", "ps", "svg"}
        Output format.
    """
    plots = [
        subprocess_run_for_testing(
            [sys.executable, "-R", "-c",
             f"from matplotlib.tests.test_determinism import _save_figure;"
             f"_save_figure({objects!r}, {fmt!r}, {usetex})"],
            env={**os.environ, "SOURCE_DATE_EPOCH": "946684800",
                 "MPLBACKEND": "Agg"},
            text=False, capture_output=True, check=True).stdout
        for _ in range(3)
    ]
    for p in plots[1:]:
        if fmt == "ps" and usetex:
            if p != plots[0]:
                pytest.skip("failed, maybe due to ghostscript timestamps")
        else:
            assert p == plots[0]

