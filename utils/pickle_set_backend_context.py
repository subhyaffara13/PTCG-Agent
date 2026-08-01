
def pickle_set_backend_context(ctx):
    return _SetBackendContext, ctx._pickle()

