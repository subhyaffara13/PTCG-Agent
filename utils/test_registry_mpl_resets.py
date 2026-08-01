
def test_registry_mpl_resets():
    # Check that Matplotlib converters are properly reset (see issue #27481)
    code = (
        "import matplotlib.units as units; "
        "import matplotlib.dates as mdates; "
        "n_conv = len(units.registry); "
        "import pandas as pd; "
        "pd.plotting.register_matplotlib_converters(); "
        "pd.plotting.deregister_matplotlib_converters(); "
        "assert len(units.registry) == n_conv"
    )
    call = [sys.executable, "-c", code]
    subprocess.check_output(call)

