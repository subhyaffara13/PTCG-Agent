
def _create_qApp():
    app = QtWidgets.QApplication.instance()

    # Create a new QApplication and configure it if none exists yet, as only
    # one QApplication can exist at a time.
    if app is None:
        # display_is_valid returns False only if on Linux and neither X11
        # nor Wayland display can be opened.
        if not mpl._c_internal_utils.display_is_valid():
            raise RuntimeError('Invalid DISPLAY variable')

        # Check to make sure a QApplication from a different major version
        # of Qt is not instantiated in the process
        if QT_API in {'PyQt6', 'PySide6'}:
            other_bindings = ('PyQt5', 'PySide2')
            qt_version = 6
        elif QT_API in {'PyQt5', 'PySide2'}:
            other_bindings = ('PyQt6', 'PySide6')
            qt_version = 5
        else:
            raise RuntimeError("Should never be here")

        for binding in other_bindings:
            mod = sys.modules.get(f'{binding}.QtWidgets')
            if mod is not None and mod.QApplication.instance() is not None:
                other_core = sys.modules.get(f'{binding}.QtCore')
                _api.warn_external(
                    f'Matplotlib is using {QT_API} which wraps '
                    f'{QtCore.qVersion()} however an instantiated '
                    f'QApplication from {binding} which wraps '
                    f'{other_core.qVersion()} exists.  Mixing Qt major '
                    'versions may not work as expected.'
                )
                break
        if qt_version == 5:
            try:
                QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
            except AttributeError:  # Only for Qt>=5.6, <6.
                pass
        try:
            QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
                QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        except AttributeError:  # Only for Qt>=5.14.
            pass
        app = QtWidgets.QApplication(["matplotlib"])
        if sys.platform == "darwin":
            image = str(cbook._get_data_path('images/matplotlib.svg'))
            icon = QtGui.QIcon(image)
            app.setWindowIcon(icon)
        app.setQuitOnLastWindowClosed(True)
        cbook._setup_new_guiapp()
        if qt_version == 5:
            app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    return app

