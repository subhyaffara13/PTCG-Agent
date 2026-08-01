
def save_sys_modules():
    """Make sure initial ``sys.modules`` is preserved"""
    prev_modules = sys.modules

    try:
        sys.modules = sys.modules.copy()
        yield
    finally:
        sys.modules = prev_modules

