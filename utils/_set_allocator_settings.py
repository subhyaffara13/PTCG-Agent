
def _set_allocator_settings(env: str):
    # pyrefly: ignore [missing-attribute]
    return torch._C._accelerator_setAllocatorSettings(env)

