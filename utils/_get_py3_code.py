import os

def _get_py3_code(code, fn_name):
    with tempfile.TemporaryDirectory() as tmp_dir:
        script_path = os.path.join(tmp_dir, 'script.py')
        with open(script_path, 'w') as f:
            f.write(code)
        spec = importlib.util.spec_from_file_location(fn_name, script_path)
        module = importlib.util.module_from_spec(spec)
        loader = spec.loader
        if not isinstance(loader, Loader):  # Assert type to meet MyPy requirement
            raise AssertionError(f"Expected loader to be Loader, got {type(loader)}")
        loader.exec_module(module)
        fn = getattr(module, fn_name)
        return fn

