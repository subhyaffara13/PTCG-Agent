
def _test_module_getattr():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=ImportWarning)
    module_name = sys.argv[1]
    _test_getattr(module_name, use_pytest=False)

