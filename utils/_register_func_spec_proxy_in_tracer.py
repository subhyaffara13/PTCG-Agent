
def _register_func_spec_proxy_in_tracer(tracer, name, spec):
    """
    This is a wrapper utility method on top of tracer to cache the
    already registered subclass spec attribute. This is useful because
    Subclass.__init__ will be same for each subclass. By default, fx will
    create multiple attributes/proxies for given attribute.
    """
    fx_name = name + "0"
    if hasattr(tracer.root, fx_name):
        if getattr(tracer.root, fx_name) != spec:
            raise AssertionError(f"spec mismatch for {fx_name}")
        return tracer.create_proxy("get_attr", fx_name, (), {})

    qualname = tracer.get_fresh_qualname(name)
    setattr(tracer.root, qualname, spec)
    return tracer.create_proxy("get_attr", qualname, (), {})

