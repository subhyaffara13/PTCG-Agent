
def get_module_method(m, module, method):
    return m._c.getattr(module)._get_method(method)

