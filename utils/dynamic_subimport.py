
def dynamic_subimport(name, vars):
    mod = types.ModuleType(name)
    mod.__dict__.update(vars)
    mod.__dict__["__builtins__"] = builtins.__dict__
    return mod

