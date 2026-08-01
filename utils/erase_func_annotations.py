
def erase_func_annotations(func: FuncDef) -> None:
    func.type_args = None
    for arg in func.arguments:
        arg.type_annotation = None
        arg.variable.type = None
    func.type = None
    func.unanalyzed_type = None

