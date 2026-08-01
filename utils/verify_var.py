
def verify_var(
    stub: nodes.Var, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    if isinstance(runtime, Missing):
        # Don't always yield an error here, because we often can't find instance variables
        if len(object_path) <= 2:
            yield Error(object_path, "is not present at runtime", stub, runtime)
        return

    if (
        stub.is_initialized_in_class
        and is_read_only_property(runtime)
        and (stub.is_settable_property or not stub.is_property)
    ):
        yield Error(object_path, "is read-only at runtime but not in the stub", stub, runtime)

    runtime_type = get_mypy_type_of_runtime_value(runtime, type_context=stub.type)
    note = ""
    if (
        runtime_type is not None
        and stub.type is not None
        and not is_subtype_helper(runtime_type, stub.type)
    ):
        should_error = True
        # Avoid errors when defining enums, since runtime_type is the enum itself, but we'd
        # annotate it with the type of runtime.value
        if isinstance(runtime, enum.Enum):
            runtime_type = get_mypy_type_of_runtime_value(runtime.value)
            if runtime_type is not None and is_subtype_helper(runtime_type, stub.type):
                should_error = False
            # We always allow setting the stub value to Ellipsis (...), but use
            # _value_ type as a fallback if given. If a member is ... and _value_
            # type is given, all runtime types should be assignable to _value_.
            proper_type = mypy.types.get_proper_type(stub.type)
            if (
                isinstance(proper_type, mypy.types.Instance)
                and proper_type.type.fullname in mypy.types.ELLIPSIS_TYPE_NAMES
            ):
                value_t = stub.info.get("_value_")
                if value_t is None or value_t.type is None or runtime_type is None:
                    should_error = False
                elif is_subtype_helper(runtime_type, value_t.type):
                    should_error = False
                else:
                    note = " (incompatible '_value_')"

        if should_error:
            yield Error(
                object_path,
                f"variable differs from runtime type {runtime_type}{note}",
                stub,
                runtime,
            )
    elif stub.final_value is not None and stub.final_value != runtime:
        yield Error(
            object_path,
            "is inconsistent, stub value for Final var differs from runtime value",
            stub,
            runtime,
            stub_desc=repr(stub.final_value),
        )

