
def _test_getattr(module_name, use_pytest=True):
    """
    Test that __getattr__ methods raise AttributeError for unknown keys.
    See #20822, #20855.
    """
    try:
        module = import_module(module_name)
    except (ImportError, RuntimeError, OSError) as e:
        # Skip modules that cannot be imported due to missing dependencies
        if use_pytest:
            pytest.skip(f'Cannot import {module_name} due to {e}')
        else:
            print(f'SKIP: Cannot import {module_name} due to {e}')
            return

    key = 'THIS_SYMBOL_SHOULD_NOT_EXIST'
    if hasattr(module, key):
        delattr(module, key)

