
def translate_set_from_generator_call(
    builder: IRBuilder, expr: CallExpr, callee: RefExpr
) -> Value | None:
    """Special case for set creation from a generator.

    For example:
        set(f(...) for ... in iterator/nested_generators...)
    """
    if (
        len(expr.args) == 1
        and expr.arg_kinds[0] == ARG_POS
        and isinstance(expr.args[0], GeneratorExpr)
    ):
        return translate_set_comprehension(builder, expr.args[0])
    return None

