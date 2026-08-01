
def fallback_dispatcher(func, types, args, kwargs):
    with no_dispatch():
        return func(*args)

