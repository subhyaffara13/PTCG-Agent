
def make_builder(
    *,
    module_name: str = "pkg.current",
    native_modules: set[str] | None = None,
    same_group_modules: set[str] | None = None,
    graph: set[str] | None = None,
) -> IRBuilder:
    native_modules = native_modules or set()
    same_group_modules = same_group_modules or set()
    group_map: dict[str, str | None] = {module_name: "current-group"}
    for module in native_modules:
        group_map[module] = "current-group" if module in same_group_modules else "other-group"

    errors = Errors(Options())
    current_file = MypyFile([], [])
    current_file._fullname = module_name
    pbv = PreBuildVisitor(errors, current_file, {}, {})
    builder = IRBuilder(
        module_name,
        {},
        cast(Graph, {name: object() for name in (graph or set())}),
        errors,
        Mapper(group_map),
        pbv,
        IRBuilderVisitor(),
        CompilerOptions(),
        {},
    )
    builder.set_module(module_name, module_name.replace(".", "/") + ".py")
    return builder

