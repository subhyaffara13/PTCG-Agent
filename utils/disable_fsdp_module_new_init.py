
def disable_fsdp_module_new_init() -> Iterator[None]:
    global _enable_fsdp_module_new_init
    prev, _enable_fsdp_module_new_init = _enable_fsdp_module_new_init, False
    try:
        yield
    finally:
        _enable_fsdp_module_new_init = prev

