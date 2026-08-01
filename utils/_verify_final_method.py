
def _verify_final_method(
    stub: nodes.FuncDef, runtime: Any, static_runtime: MaybeMissing[Any]
) -> Iterator[str]:
    if stub.is_final:
        return
    if getattr(runtime, "__final__", False) or (
        static_runtime is not MISSING and getattr(static_runtime, "__final__", False)
    ):
        yield "is decorated with @final at runtime, but not in the stub"

