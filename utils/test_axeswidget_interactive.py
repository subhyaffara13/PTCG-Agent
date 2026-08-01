
def test_axeswidget_interactive():
    subprocess_run_helper(
        _test_axeswidget_interactive,
        timeout=120 if is_ci_environment() else 20,
        extra_env={'MPLBACKEND': 'tkagg'}
    )

