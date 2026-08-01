
def _get_available_interactive_backends():
    _is_linux_and_display_invalid = (sys.platform == "linux" and
                                     not _c_internal_utils.display_is_valid())
    _is_linux_and_xdisplay_invalid = (sys.platform == "linux" and
                                      not _c_internal_utils.xdisplay_is_valid())
    envs = []
    for deps, env in [
            *[([qt_api],
               {"MPLBACKEND": "qtagg", "QT_API": qt_api})
              for qt_api in ["PyQt6", "PySide6", "PyQt5", "PySide2"]],
            *[([qt_api, "cairocffi"],
               {"MPLBACKEND": "qtcairo", "QT_API": qt_api})
              for qt_api in ["PyQt6", "PySide6", "PyQt5", "PySide2"]],
            *[(["cairo", "gi"], {"MPLBACKEND": f"gtk{version}{renderer}"})
              for version in [3, 4] for renderer in ["agg", "cairo"]],
            (["tkinter"], {"MPLBACKEND": "tkagg"}),
            (["wx"], {"MPLBACKEND": "wx"}),
            (["wx"], {"MPLBACKEND": "wxagg"}),
            (["matplotlib.backends._macosx"], {"MPLBACKEND": "macosx"}),
    ]:
        reason = None
        missing = [dep for dep in deps if not importlib.util.find_spec(dep)]
        if missing:
            reason = "{} cannot be imported".format(", ".join(missing))
        elif _is_linux_and_xdisplay_invalid and (
                env["MPLBACKEND"] == "tkagg"
                # Remove when https://github.com/wxWidgets/Phoenix/pull/2638 is out.
                or env["MPLBACKEND"].startswith("wx")):
            reason = "$DISPLAY is unset"
        elif _is_linux_and_display_invalid:
            reason = "$DISPLAY and $WAYLAND_DISPLAY are unset"
        elif env["MPLBACKEND"] == 'macosx' and os.environ.get('TF_BUILD'):
            reason = "macosx backend fails on Azure"
        elif env["MPLBACKEND"].startswith('gtk'):
            try:
                import gi
            except ImportError:
                # Though we check that `gi` exists above, it is possible that its
                # C-level dependencies are not available, and then it still raises an
                # `ImportError`, so guard against that.
                available_gtk_versions = []
            else:
                gi_repo = gi.Repository.get_default()
                available_gtk_versions = gi_repo.enumerate_versions('Gtk')
            version = env["MPLBACKEND"][3]
            if f'{version}.0' not in available_gtk_versions:
                reason = "no usable GTK bindings"
        marks = []
        if reason:
            marks.append(pytest.mark.skip(reason=f"Skipping {env} because {reason}"))
        elif env["MPLBACKEND"].startswith('wx') and sys.platform == 'darwin':
            # ignore on macosx because that's currently broken (github #16849)
            marks.append(pytest.mark.xfail(reason='github #16849'))

        envs.append(({**env, 'BACKEND_DEPS': ','.join(deps)}, marks))
    return envs

