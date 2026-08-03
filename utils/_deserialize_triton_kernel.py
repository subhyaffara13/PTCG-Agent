from typing import Any

def _deserialize_triton_kernel(kernel_info: tuple[str, str]) -> Any:
    """
    Deserialize a triton kernel by reimporting from its module.
    kernel_info is (module_path, function_name) tuple.
    """
    module_path, func_name = kernel_info
    module = importlib.import_module(module_path)
    kernel = getattr(module, func_name)
    return kernel

