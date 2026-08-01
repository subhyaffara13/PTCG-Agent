
def verify_typealias(
    stub: nodes.TypeAlias, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    stub_target = mypy.types.get_proper_type(stub.target)
    stub_desc = f"Type alias for {stub_target}"
    if isinstance(runtime, Missing):
        yield Error(object_path, "is not present at runtime", stub, runtime, stub_desc=stub_desc)
        return
    runtime_origin = get_origin(runtime) or runtime
    if isinstance(stub_target, mypy.types.Instance):
        if not isinstance(runtime_origin, type):
            yield Error(
                object_path,
                "is inconsistent, runtime is not a type",
                stub,
                runtime,
                stub_desc=stub_desc,
            )
            return

        stub_origin = stub_target.type
        # Do our best to figure out the fullname of the runtime object...
        runtime_name: object
        try:
            runtime_name = runtime_origin.__qualname__
        except AttributeError:
            runtime_name = getattr(runtime_origin, "__name__", MISSING)
        if isinstance(runtime_name, str):
            runtime_module: object = getattr(runtime_origin, "__module__", MISSING)
            if isinstance(runtime_module, str):
                if runtime_module == "collections.abc" or (
                    runtime_module == "re" and runtime_name in {"Match", "Pattern"}
                ):
                    runtime_module = "typing"
                runtime_fullname = f"{runtime_module}.{runtime_name}"
                if re.fullmatch(rf"_?{re.escape(stub_origin.fullname)}", runtime_fullname):
                    # Okay, we're probably fine.
                    return

        # Okay, either we couldn't construct a fullname
        # or the fullname of the stub didn't match the fullname of the runtime.
        # Fallback to a full structural check of the runtime vis-a-vis the stub.
        yield from verify_typeinfo(stub_origin, runtime_origin, object_path, is_alias_target=True)
        return
    if isinstance(stub_target, mypy.types.UnionType):
        # complain if runtime is not a Union or UnionType
        if runtime_origin is not Union and not isinstance(runtime, types.UnionType):
            yield Error(object_path, "is not a Union", stub, runtime, stub_desc=str(stub_target))
        # could check Union contents here...
        return
    if isinstance(stub_target, mypy.types.TupleType):
        if tuple not in getattr(runtime_origin, "__mro__", ()):
            yield Error(
                object_path, "is not a subclass of tuple", stub, runtime, stub_desc=stub_desc
            )
        # could check Tuple contents here...
        return
    if isinstance(stub_target, mypy.types.CallableType):
        if runtime_origin is not collections.abc.Callable:
            yield Error(
                object_path, "is not a type alias for Callable", stub, runtime, stub_desc=stub_desc
            )
        # could check Callable contents here...
        return
    if isinstance(stub_target, mypy.types.AnyType):
        return
    yield Error(object_path, "is not a recognised type alias", stub, runtime, stub_desc=stub_desc)

