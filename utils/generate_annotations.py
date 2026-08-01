
def generate_annotations(
    path: str, tree: MypyFile, ir: ModuleIR, type_map: dict[Expression, Type], mapper: Mapper
) -> AnnotatedSource:
    anns = {}
    for func_ir in ir.functions:
        anns.update(function_annotations(func_ir, tree))
    visitor = ASTAnnotateVisitor(type_map, mapper)
    for defn in tree.defs:
        defn.accept(visitor)
    anns.update(visitor.anns)
    for line in visitor.ignored_lines:
        if line in anns:
            del anns[line]
    return AnnotatedSource(path, anns)

