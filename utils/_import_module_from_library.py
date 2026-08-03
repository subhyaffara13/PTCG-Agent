import os

def _import_module_from_library(module_name, path, is_python_module):
    filepath = os.path.join(path, f"{module_name}{LIB_EXT}")
    if is_python_module:
        # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None:
            raise AssertionError(f"Failed to create spec for module {module_name} at {filepath}")
        module = importlib.util.module_from_spec(spec)
        if not isinstance(spec.loader, importlib.abc.Loader):
            raise AssertionError("spec.loader is not a valid importlib Loader")
        spec.loader.exec_module(module)
        return module
    else:
        torch.ops.load_library(filepath)
        return filepath

