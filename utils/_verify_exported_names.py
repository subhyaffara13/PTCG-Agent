
def _verify_exported_names(
    object_path: list[str], stub: nodes.MypyFile, runtime_all_as_set: set[str]
) -> Iterator[Error]:
    # note that this includes the case the stub simply defines `__all__: list[str]`
    assert "__all__" in stub.names
    public_names_in_stub = {m for m, o in stub.names.items() if o.module_public}
    names_in_stub_not_runtime = sorted(public_names_in_stub - runtime_all_as_set)
    names_in_runtime_not_stub = sorted(runtime_all_as_set - public_names_in_stub)
    if not (names_in_runtime_not_stub or names_in_stub_not_runtime):
        return
    yield Error(
        object_path + ["__all__"],
        (
            "names exported from the stub do not correspond to the names exported at runtime. "
            "This is probably due to things being missing from the stub or an inaccurate `__all__` in the stub"
        ),
        # Pass in MISSING instead of the stub and runtime objects, as the line numbers aren't very
        # relevant here, and it makes for a prettier error message
        # This means this error will be ignored when using `--ignore-missing-stub`, which is
        # desirable in at least the `names_in_runtime_not_stub` case
        stub_object=MISSING,
        runtime_object=MISSING,
        stub_desc=(f"Names exported in the stub but not at runtime: {names_in_stub_not_runtime}"),
        runtime_desc=(
            f"Names exported at runtime but not in the stub: {names_in_runtime_not_stub}"
        ),
    )

