from typing import Callable

def resolve_internal_import(module: ModuleType | None, chained_path: str) -> Callable | ModuleType | None:
    """
    Check if a given `module` has an internal import path as defined by the `chained_path`.
    This can either be the full path (not exposed in `__init__`) OR the last part of the chain (exposed in `__init__`).

    This is an important helper function for kernels based modules to apply the import from the module
    itself, i.e. stay compatible with original libraries in certain cases.

    Example:
        Module: `mamba_ssm`
        Chained Path: `ops.triton.selective_state_update.selective_state_update`
        Resulting import attempt at:
            - `mamba_ssm.selective_state_update`
            - `mamba_ssm.ops.triton.selective_state_update.selective_state_update`
    """
    if not module:
        return None

    if final_module := getattr(module, chained_path.split(".")[-1], None):
        return final_module

    final_module = module
    for path in chained_path.split("."):
        final_module = getattr(final_module, path, None)
        if not final_module:
            return None

    return final_module

