
def pickle_skip_backend_context(ctx):
    return _SkipBackendContext, ctx._pickle()

