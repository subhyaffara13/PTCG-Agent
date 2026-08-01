
def build_conditional_library(
    lib: typing.Any,
    conditional_names: Mapping[str, Callable[[], list[str]]],
) -> typing.Any:
    conditional_lib = types.ModuleType("lib")
    conditional_lib._original_lib = lib  # type: ignore[attr-defined]
    excluded_names = set()
    for condition, names_cb in conditional_names.items():
        if not getattr(lib, condition):
            excluded_names.update(names_cb())

    for attr in dir(lib):
        if attr not in excluded_names:
            setattr(conditional_lib, attr, getattr(lib, attr))

    return conditional_lib

