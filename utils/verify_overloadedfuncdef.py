
def verify_overloadedfuncdef(
    stub: nodes.OverloadedFuncDef, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    # TODO: support `@type_check_only` decorator
    if isinstance(runtime, Missing):
        yield Error(object_path, "is not present at runtime", stub, runtime)
        return

    if stub.is_property:
        # Any property with a setter is represented as an OverloadedFuncDef
        if is_read_only_property(runtime):
            yield Error(object_path, "is read-only at runtime but not in the stub", stub, runtime)
        return

    if not is_probably_a_function(runtime):
        yield Error(object_path, "is not a function", stub, runtime)
        if not callable(runtime):
            return

    # mypy doesn't allow overloads where one overload is abstract but another isn't,
    # so it should be okay to just check whether the first overload is abstract or not.
    #
    # TODO: Mypy *does* allow properties where e.g. the getter is abstract but the setter is not;
    # and any property with a setter is represented as an OverloadedFuncDef internally;
    # not sure exactly what (if anything) we should do about that.
    first_part = stub.items[0]
    if isinstance(first_part, nodes.Decorator) and first_part.is_overload:
        for msg in _verify_abstract_status(first_part.func, runtime):
            yield Error(object_path, msg, stub, runtime)

    # Look the object up statically, to avoid binding by the descriptor protocol
    static_runtime = _static_lookup_runtime(object_path)

    for message in _verify_static_class_methods(stub, runtime, static_runtime, object_path):
        yield Error(object_path, "is inconsistent, " + message, stub, runtime)

    # TODO: Should call _verify_final_method here,
    # but overloaded final methods in stubs cause a stubtest crash: see #14950

    signature = safe_inspect_signature(runtime)
    if not signature:
        return

    stub_sig = Signature.from_overloadedfuncdef(stub)
    runtime_sig = Signature.from_inspect_signature(signature)

    for message in _verify_signature(
        stub_sig,
        runtime_sig,
        function_name=stub.name,
        warn_runtime_is_object_init=runtime is object.__init__,
    ):
        # TODO: This is a little hacky, but the addition here is super useful
        if "has a default value of type" in message:
            message += (
                ". This is often caused by overloads failing to account for explicitly passing "
                "in the default value."
            )
        yield Error(
            object_path,
            "is inconsistent, " + message,
            stub,
            runtime,
            stub_desc=(str(stub.type)) + f"\nInferred signature: {stub_sig}",
            runtime_desc="def " + str(signature),
        )

