
def get_gpu_shared_memory() -> int:
    from triton.runtime import driver

    return driver.active.utils.get_device_properties(0).get("max_shared_mem", 0)

