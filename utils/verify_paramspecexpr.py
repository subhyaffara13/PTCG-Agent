from typing import Any

def verify_paramspecexpr(
    stub: nodes.ParamSpecExpr, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    if isinstance(runtime, Missing):
        yield Error(object_path, "is not present at runtime", stub, runtime)
        return
    maybe_paramspec_types = (
        getattr(typing, "ParamSpec", None),
        getattr(typing_extensions, "ParamSpec", None),
    )
    paramspec_types = tuple(t for t in maybe_paramspec_types if t is not None)
    if not paramspec_types or not isinstance(runtime, paramspec_types):
        yield Error(object_path, "is not a ParamSpec", stub, runtime)
        return

