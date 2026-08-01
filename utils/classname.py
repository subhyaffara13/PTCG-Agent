
def classname(func: FunctionSchema, with_namespace: bool = False) -> str:
    namespace = "at::functionalization::" if with_namespace else ""
    return f"{namespace}{func.name.unambiguous_name()}_ViewMeta"

