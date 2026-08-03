from typing import Any, Callable

def extract_bw_module(CompiledFunction: Any) -> Callable[..., Any]:
    if isinstance(
        CompiledFunction._lazy_backward_info, AutogradLazyBackwardCompileInfo
    ):
        return CompiledFunction._lazy_backward_info.bw_module
    elif isinstance(
        CompiledFunction._lazy_backward_info, CachedAutogradLazyBackwardCompileInfo
    ):
        with torch._subclasses.fake_tensor.unset_fake_temporarily():
            return CompiledFunction._lazy_backward_info.bw_module_fn()
    else:
        raise AssertionError(
            "Unexpected Lazy Backward Compilation Info Type. Please file an issue."
        )

