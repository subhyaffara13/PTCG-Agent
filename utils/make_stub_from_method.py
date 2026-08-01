
def make_stub_from_method(nn_module, method_name):
    func = getattr(nn_module, method_name)
    if isinstance(func, ScriptMethodStub):
        return func
    # Make sure the name present in the resulting AST will match the name
    # requested here. The only time they don't match is if you do something
    # like:
    #   def _forward(self):
    #       pass
    #   forward = _forward
    # In this case, the actual function object will have the name `_forward`,
    # even though we requested a stub for `forward`.
    return make_stub(func, method_name)

