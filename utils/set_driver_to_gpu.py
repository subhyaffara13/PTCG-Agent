
def set_driver_to_gpu():
    driver = triton.runtime.driver
    for name, backend in triton.backends.backends.items():
        if _is_backend_active(name, backend) and name != "cpu":
            # After https://github.com/triton-lang/triton/commit/b844d519bc5e86edf00fe6b3c6c2d1badcd509a4,
            # `driver.active` can be of `LazyProxy` type and the sign of this - `_obj` attribute.
            if (
                isinstance(driver.active, backend.driver)
                or hasattr(driver.active, "_obj")
                and isinstance(driver.active._obj, backend.driver)
            ):
                # Don't re-initialize backend if it is already active
                return
            driver.set_active(backend.driver())
            return
    raise RuntimeError("Could not find an active GPU backend")

