
def translate_dataclasses_field_call(
    builder: IRBuilder, expr: CallExpr, callee: RefExpr
) -> Value | None:
    """Special case for 'dataclasses.field', 'attr.attrib', and 'attr.Factory'
    function calls because the results of such calls are type-checked
    by mypy using the types of the arguments to their respective
    functions, resulting in attempted coercions by mypyc that throw a
    runtime error.
    """
    builder.types[expr] = AnyType(TypeOfAny.from_error)
    return None

