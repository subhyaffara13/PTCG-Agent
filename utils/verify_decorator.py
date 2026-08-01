
def verify_decorator(
    stub: nodes.Decorator, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    if stub.func.is_type_check_only:
        # This function only exists in stubs, we only check that the runtime part
        # is missing. Other checks are not required.
        if not isinstance(runtime, Missing):
            yield Error(
                object_path,
                'is marked as "@type_check_only", but also exists at runtime',
                stub,
                runtime,
                stub_desc=repr(stub),
            )
        return

    if isinstance(runtime, Missing):
        yield Error(object_path, "is not present at runtime", stub, runtime)
        return
    if stub.func.is_property:
        for message in _verify_readonly_property(stub, runtime):
            yield Error(object_path, message, stub, runtime)
        for message in _verify_abstract_status(stub.func, runtime):
            yield Error(object_path, message, stub, runtime)
        return

    func = _resolve_funcitem_from_decorator(stub)
    if func is not None:
        yield from verify(func, runtime, object_path)

