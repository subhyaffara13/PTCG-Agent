
def verify_typeinfo(
    stub: nodes.TypeInfo,
    runtime: MaybeMissing[type[Any]],
    object_path: list[str],
    *,
    is_alias_target: bool = False,
) -> Iterator[Error]:
    if stub.is_type_check_only and not is_alias_target:
        # This type only exists in stubs, we only check that the runtime part
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
        msg = "is not present at runtime"
        if is_probably_private(stub.name):
            msg += '. Maybe mark it as "@type_check_only"?'
        yield Error(object_path, msg, stub, runtime, stub_desc=repr(stub))
        return
    if not isinstance(runtime, type):
        # Yes, some runtime objects can be not types, no way to tell mypy about that.
        yield Error(object_path, "is not a type", stub, runtime, stub_desc=repr(stub))  # type: ignore[unreachable]
        return

    yield from _verify_final(stub, runtime, object_path)
    yield from _verify_disjoint_base(stub, runtime, object_path)
    is_runtime_typeddict = stub.typeddict_type is not None and is_typeddict(runtime)
    yield from _verify_metaclass(
        stub, runtime, object_path, is_runtime_typeddict=is_runtime_typeddict
    )

    # Check everything already defined on the stub class itself (i.e. not inherited)
    #
    # Filter out non-identifier names, as these are (hopefully always?) whacky/fictional things
    # (like __mypy-replace or __mypy-post_init, etc.) that don't exist at runtime,
    # and exist purely for internal mypy reasons
    to_check = {name for name in stub.names if name.isidentifier()}
    # Check all public things on the runtime class
    to_check.update(
        m for m in vars(runtime) if not is_probably_private(m) and m not in IGNORABLE_CLASS_DUNDERS
    )
    # Special-case the __init__ method for Protocols and the __new__ method for TypedDicts
    #
    # TODO: On Python <3.11, __init__ methods on Protocol classes
    # are silently discarded and replaced.
    # However, this is not the case on Python 3.11+.
    # Ideally, we'd figure out a good way of validating Protocol __init__ methods on 3.11+.
    if stub.is_protocol:
        to_check.discard("__init__")
    if is_runtime_typeddict:
        to_check.discard("__new__")

    for entry in sorted(to_check):
        mangled_entry = entry
        if entry.startswith("__") and not entry.endswith("__"):
            mangled_entry = f"_{stub.name.lstrip('_')}{entry}"
        stub_to_verify = next((t.names[entry].node for t in stub.mro if entry in t.names), MISSING)
        assert stub_to_verify is not None
        try:
            try:
                runtime_attr = getattr(runtime, mangled_entry)
            except AttributeError:
                runtime_attr = inspect.getattr_static(runtime, mangled_entry, MISSING)
        except Exception:
            # Catch all exceptions in case the runtime raises an unexpected exception
            # from __getattr__ or similar.
            continue

        # If it came from the metaclass, consider the runtime_attr to be MISSING
        # for a more accurate message
        if (
            runtime_attr is not MISSING
            and type(runtime) is not runtime
            and getattr(runtime_attr, "__objclass__", None) is type(runtime)
        ):
            runtime_attr = MISSING

        # __setattr__ and __delattr__ on object are a special case,
        # so if we only have these methods inherited from there, pretend that
        # we don't have them. See python/typeshed#7385.
        if (
            entry in ("__setattr__", "__delattr__")
            and runtime_attr is not MISSING
            and runtime is not object
            and getattr(runtime_attr, "__objclass__", None) is object
        ):
            runtime_attr = MISSING

        # Do not error for an object missing from the stub
        # If the runtime object is a types.WrapperDescriptorType object
        # and has a non-special dunder name.
        # The vast majority of these are false positives.
        if not (
            isinstance(stub_to_verify, Missing)
            and isinstance(runtime_attr, types.WrapperDescriptorType)
            and is_dunder(mangled_entry, exclude_special=True)
        ):
            yield from verify(stub_to_verify, runtime_attr, object_path + [entry])

