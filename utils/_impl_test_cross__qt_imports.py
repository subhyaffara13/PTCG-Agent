
def _impl_test_cross_Qt_imports():
    import importlib
    import sys
    import warnings

    _, host_binding, mpl_binding = sys.argv
    # import the mpl binding.  This will force us to use that binding
    importlib.import_module(f'{mpl_binding}.QtCore')
    mpl_binding_qwidgets = importlib.import_module(f'{mpl_binding}.QtWidgets')
    import matplotlib.backends.backend_qt
    host_qwidgets = importlib.import_module(f'{host_binding}.QtWidgets')

    host_app = host_qwidgets.QApplication(["mpl testing"])
    warnings.filterwarnings("error", message=r".*Mixing Qt major.*",
                            category=UserWarning)
    matplotlib.backends.backend_qt._create_qApp()

