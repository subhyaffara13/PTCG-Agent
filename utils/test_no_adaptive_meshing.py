
def test_no_adaptive_meshing():
    matplotlib = import_module('matplotlib', min_module_version='1.1.0', catch=(RuntimeError,))
    if matplotlib:
        try:
            temp_dir = mkdtemp()
            TmpFileManager.tmp_folder(temp_dir)
            x = Symbol('x')
            y = Symbol('y')
            # Test plots which cannot be rendered using the adaptive algorithm

            # This works, but it triggers a deprecation warning from sympify(). The
            # code needs to be updated to detect if interval math is supported without
            # relying on random AttributeErrors.
            with warns(UserWarning, match="Adaptive meshing could not be applied"):
                plot_and_save(Eq(y, re(cos(x) + I*sin(x))), name='test', dir=temp_dir)
        finally:
            TmpFileManager.cleanup()
    else:
        skip("Matplotlib not the default backend")

