import os
import sys

def test_openin_any_paranoid():
    completed = subprocess_run_for_testing(
        [sys.executable, "-c",
         'import matplotlib.pyplot as plt;'
         'plt.rcParams.update({"text.usetex": True});'
         'plt.title("paranoid");'
         'plt.gcf().canvas.draw();'],
        env={**os.environ, 'MPLBACKEND': 'Agg', 'openin_any': 'p'},
        check=True, capture_output=True)
    assert completed.stderr == ""

