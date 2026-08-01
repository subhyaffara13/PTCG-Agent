
def get_backend_options():
    from triton.runtime import driver

    target = driver.active.get_current_target()
    backend = triton.compiler.compiler.make_backend(target)
    options = backend.parse_options(dict())
    return options.__dict__

