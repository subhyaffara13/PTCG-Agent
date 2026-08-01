
def convert_overload_part(self: OverloadPart) -> Json:
    if isinstance(self, FuncDef):
        return convert_func_def(self)
    else:
        return convert_decorator(self)

