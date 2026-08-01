
def _contains_fake_script_object(obj) -> bool:
    """Check if obj is or contains a FakeScriptObject.
    This is load-bearing for TorchBindOpOverloads so we avoid pytree
    since it's much slower.
    """
    if isinstance(obj, torch._library.fake_class_registry.FakeScriptObject):
        return True
    elif isinstance(obj, (list, tuple)):
        return any(_contains_fake_script_object(item) for item in obj)
    elif isinstance(obj, dict):
        return any(_contains_fake_script_object(v) for v in obj.values())
    return False

