
def test_matplotlib():
    matplotlib = import_module('matplotlib', min_module_version='1.1.0', catch=(RuntimeError,))
    if matplotlib:
        try:
            plot_implicit_tests('test')
            test_line_color()
        finally:
            TmpFileManager.cleanup()
    else:
        skip("Matplotlib not the default backend")

