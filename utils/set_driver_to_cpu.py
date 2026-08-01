
def set_driver_to_cpu():
    driver = triton.runtime.driver
    if backend := triton.backends.backends.get("cpu", None):
        if isinstance(driver.active, backend.driver):
            # Don't re-initialize backend if it is already active
            return
        driver.set_active(backend.driver())
        return
    # This can be a hard error once triton-cpu is merged into fbcode
    warnings.warn(
        "Could not find an active CPU backend. Generated kernels will not be executable!"
    )

