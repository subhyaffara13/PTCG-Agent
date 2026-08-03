import os
import sys

def test_importable_with__OO():
    """
    When using -OO or export PYTHONOPTIMIZE=2, docstrings are discarded,
    this simple test may prevent something like issue #17970.
    """
    program = (
        "import matplotlib as mpl; "
        "import matplotlib.pyplot as plt; "
        "import matplotlib.cbook as cbook; "
        "import matplotlib.patches as mpatches"
    )
    subprocess_run_for_testing(
        [sys.executable, "-OO", "-c", program],
        env={**os.environ, "MPLBACKEND": ""}, check=True
        )

