
def compile_unbound_method(concrete_type, fn):
    if _jit_internal.is_ignored_fn(fn):
        return None
    stub = make_stub(fn, fn.__name__)
    with torch._jit_internal._disable_emit_hooks():
        # We don't want to call the hooks here since the graph that is calling
        # this function is not yet complete
        create_methods_and_properties_from_stubs(concrete_type, (stub,), ())
    return stub

