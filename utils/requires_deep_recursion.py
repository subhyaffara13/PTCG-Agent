
def requires_deep_recursion(func):
    """Decorator to skip test if deep recursion is not supported."""
    import pytest

    @wraps(func)
    def wrapper(*args, **kwargs):
        if IS_PYSTON:
            pytest.skip("Pyston disables recursion checking")
        if IS_WASM:
            pytest.skip("WASM has limited stack size")
        if not IS_64BIT:
            pytest.skip("32 bit Python has limited stack size")
        cflags = sysconfig.get_config_var('CFLAGS') or ''
        config_args = sysconfig.get_config_var('CONFIG_ARGS') or ''
        address_sanitizer = (
            '-fsanitize=address' in cflags or
            '--with-address-sanitizer' in config_args
        )
        thread_sanitizer = (
            '-fsanitize=thread' in cflags or
            '--with-thread-sanitizer' in config_args
        )
        if address_sanitizer or thread_sanitizer:
            pytest.skip("AddressSanitizer and ThreadSanitizer do not support "
                        "deep recursion")
        return func(*args, **kwargs)
    return wrapper

