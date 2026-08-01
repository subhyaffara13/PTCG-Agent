
def reset_makefx_module_storage() -> None:
    global _makefx_next_index
    _makefx_next_index = 0
    _makefx_module_storage.clear()

