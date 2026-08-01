
def _must_dispatch_in_python(args, kwargs) -> bool:
    return any(_contains_fake_script_object(arg) for arg in args) or (
        bool(kwargs) and any(_contains_fake_script_object(v) for v in kwargs.values())
    )

