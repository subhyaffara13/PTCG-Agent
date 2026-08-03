import os
import subprocess
import sys

def test_backend_fallback_headless_invalid_backend(tmp_path):
    env = {**os.environ,
           "DISPLAY": "", "WAYLAND_DISPLAY": "",
           "MPLBACKEND": "", "MPLCONFIGDIR": str(tmp_path)}
    # plotting should fail with the tkagg backend selected in a headless environment
    with pytest.raises(subprocess.CalledProcessError):
        subprocess_run_for_testing(
            [sys.executable, "-c",
             "import matplotlib;"
             "matplotlib.use('tkagg');"
             "import matplotlib.pyplot;"
             "matplotlib.pyplot.plot(42);"
             ],
            env=env, check=True, stderr=subprocess.DEVNULL)

