
def _verify_readonly_property(stub: nodes.Decorator, runtime: Any) -> Iterator[str]:
    assert stub.func.is_property
    if isinstance(runtime, property):
        yield from _verify_final_method(stub.func, runtime.fget, MISSING)
        return
    if isinstance(runtime, functools.cached_property):
        yield from _verify_final_method(stub.func, runtime.func, MISSING)
        return
    if _is_django_cached_property(runtime):
        yield from _verify_final_method(stub.func, runtime.func, MISSING)
        return
    if inspect.isdatadescriptor(runtime):
        # It's enough like a property...
        return
    # Sometimes attributes pretend to be properties, for instance, to express that they
    # are read only. So allowlist if runtime_type matches the return type of stub.
    runtime_type = get_mypy_type_of_runtime_value(runtime)
    func_type = (
        stub.func.type.ret_type if isinstance(stub.func.type, mypy.types.CallableType) else None
    )
    if (
        runtime_type is not None
        and func_type is not None
        and is_subtype_helper(runtime_type, func_type)
    ):
        return
    yield "is inconsistent, cannot reconcile @property on stub with runtime object"

