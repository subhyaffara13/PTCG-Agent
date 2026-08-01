
def _test_args(obj):
    all_basic = all(isinstance(arg, Basic) for arg in obj.args)
    # Ideally obj.func(*obj.args) would always recreate the object, but for
    # now, we only require it for objects with non-empty .args
    recreatable = not obj.args or obj.func(*obj.args) == obj
    return all_basic and recreatable

