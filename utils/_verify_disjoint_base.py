
def _verify_disjoint_base(
    stub: nodes.TypeInfo, runtime: type[object], object_path: list[str]
) -> Iterator[Error]:
    is_disjoint_runtime = _is_disjoint_base(runtime)
    # Don't complain about missing @disjoint_base if there are __slots__, because
    # in that case we can infer that it's a disjoint base.
    if (
        is_disjoint_runtime
        and not stub.is_disjoint_base
        and not runtime.__dict__.get("__slots__")
        and not stub.is_final
        and not (stub.is_enum and stub.enum_members)
    ):
        yield Error(
            object_path,
            "is a disjoint base at runtime, but isn't marked with @disjoint_base in the stub",
            stub,
            runtime,
            stub_desc=repr(stub),
        )
    elif stub.is_disjoint_base:
        if not is_disjoint_runtime:
            yield Error(
                object_path,
                "is marked with @disjoint_base in the stub, but isn't a disjoint base at runtime",
                stub,
                runtime,
                stub_desc=repr(stub),
            )
        if runtime.__dict__.get("__slots__"):
            yield Error(
                object_path,
                "is marked as @disjoint_base, but also has slots; add __slots__ instead",
                stub,
                runtime,
                stub_desc=repr(stub),
            )
        elif stub.is_final:
            yield Error(
                object_path,
                "is marked as @disjoint_base, but also marked as @final; remove @disjoint_base",
                stub,
                runtime,
                stub_desc=repr(stub),
            )
        elif stub.is_enum and stub.enum_members:
            yield Error(
                object_path,
                "is marked as @disjoint_base, but is an enum with members, which is implicitly final; "
                "remove @disjoint_base",
                stub,
                runtime,
                stub_desc=repr(stub),
            )

