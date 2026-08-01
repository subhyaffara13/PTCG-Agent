
def call_torchbind_impl(obj, method, *args, **kwargs):
    if isinstance(obj, torch.ScriptObject):
        return _orig_scriptmethod_call(getattr(obj, method), *args, **kwargs)
    elif isinstance(obj, FakeScriptObject):
        return getattr(obj.wrapped_obj, method)(*args, **kwargs)
    else:
        raise RuntimeError(f"Unsupported first arg type {type(obj)} for call_torchbind")

