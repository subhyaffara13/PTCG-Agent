from typing import Any

def _assert_all_fsdp_modules(modules: Iterable[Any]) -> None:
    for module in modules:
        if not isinstance(module, FSDPModule):
            raise ValueError(f"Expects FSDPModule but got {type(module)}: {module}")

