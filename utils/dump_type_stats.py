
def dump_type_stats(
    tree: MypyFile,
    path: str,
    modules: dict[str, MypyFile],
    inferred: bool = False,
    typemap: dict[Expression, Type] | None = None,
) -> None:
    if is_special_module(path):
        return
    print(path)
    visitor = StatisticsVisitor(inferred, filename=tree.fullname, modules=modules, typemap=typemap)
    tree.accept(visitor)
    for line in visitor.output:
        print(line)
    print("  ** precision **")
    print("  precise  ", visitor.num_precise_exprs)
    print("  imprecise", visitor.num_imprecise_exprs)
    print("  any      ", visitor.num_any_exprs)
    print("  ** kinds **")
    print("  simple   ", visitor.num_simple_types)
    print("  generic  ", visitor.num_generic_types)
    print("  function ", visitor.num_function_types)
    print("  tuple    ", visitor.num_tuple_types)
    print("  TypeVar  ", visitor.num_typevar_types)
    print("  complex  ", visitor.num_complex_types)
    print("  any      ", visitor.num_any_types)

