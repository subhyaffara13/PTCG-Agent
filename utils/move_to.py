
def move_to(module, name=None):
    def decorator(func):
        if name is None:
            fname = func.__name__
        else:
            fname = name
        module.__dict__[fname] = func
        func.__module__ = module.__name__
        return func
    return decorator

