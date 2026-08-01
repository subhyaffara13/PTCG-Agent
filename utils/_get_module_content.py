
def _get_module_content(module: types.ModuleType) -> str:
    return inspect.getsource(module)

