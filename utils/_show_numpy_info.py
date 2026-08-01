
def _show_numpy_info():
    import numpy as np

    print(f"NumPy version {np.__version__}")
    info = np.lib._utils_impl._opt_info()
    print("NumPy CPU features: ", (info or 'nothing enabled'))

