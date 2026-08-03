from typing import Any

def _verify_metaclass(
    stub: nodes.TypeInfo, runtime: type[Any], object_path: list[str], *, is_runtime_typeddict: bool
) -> Iterator[Error]:
    # We exclude protocols, because of how complex their implementation is in different versions of
    # python. Enums are also hard, as are runtime TypedDicts; ignoring.
    # TODO: check that metaclasses are identical?
    if not stub.is_protocol and not stub.is_enum and not is_runtime_typeddict:
        runtime_metaclass = type(runtime)
        if runtime_metaclass is not type and stub.metaclass_type is None:
            # This means that runtime has a custom metaclass, but a stub does not.
            yield Error(
                object_path,
                "is inconsistent, metaclass differs",
                stub,
                runtime,
                stub_desc="N/A",
                runtime_desc=f"{runtime_metaclass}",
            )
        elif (
            runtime_metaclass is type
            and stub.metaclass_type is not None
            # We ignore extra `ABCMeta` metaclass on stubs, this might be typing hack.
            # We also ignore `builtins.type` metaclass as an implementation detail in mypy.
            and not mypy.types.is_named_instance(
                stub.metaclass_type, ("abc.ABCMeta", "builtins.type")
            )
        ):
            # This means that our stub has a metaclass that is not present at runtime.
            yield Error(
                object_path,
                "metaclass mismatch",
                stub,
                runtime,
                stub_desc=f"{stub.metaclass_type.type.fullname}",
                runtime_desc="N/A",
            )

