
def infer_typedDict(  # pylint: disable=invalid-name
    node: nodes.FunctionDef, ctx: context.InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Replace TypedDict FunctionDef with ClassDef."""
    class_def = nodes.ClassDef(
        name="TypedDict",
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    class_def.postinit(bases=[extract_node("dict")], body=[], decorators=None)
    func_to_add = _extract_single_node("dict")
    class_def.locals["__call__"] = [func_to_add]
    return iter([class_def])

