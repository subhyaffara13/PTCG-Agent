from typing import Any

def _serialize_triton_kernel(kernel: Any) -> tuple[str, str]:
    """
    Serialize a triton kernel by extracting its module path and function name.
    Returns (module_path, function_name) tuple.

    Triton JITFunction objects contain unpicklable _thread.RLock objects, so we
    serialize the import path instead and reimport on load.

    Raises:
        RuntimeError: If the kernel cannot be serialized (missing attributes).
    """
    fn = getattr(kernel, "fn", None)
    module_path = fn and getattr(fn, "__module__", None)
    func_name = fn and getattr(fn, "__name__", None)
    if fn is None or module_path is None or func_name is None:
        raise RuntimeError(
            f"Kernel fn missing __module__ or __name__: "
            f"module={module_path}, name={func_name}. "
            f"Cannot serialize for precompilation."
        )
    return (module_path, func_name)

