
def verify_typevarexpr(
    stub: nodes.TypeVarExpr, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    if isinstance(runtime, Missing):
        # We seem to insert these typevars into NamedTuple stubs, but they
        # don't exist at runtime. Just ignore!
        if stub.name == "_NT":
            return
        yield Error(object_path, "is not present at runtime", stub, runtime)
        return
    if not isinstance(runtime, TypeVar):
        yield Error(object_path, "is not a TypeVar", stub, runtime)
        return

