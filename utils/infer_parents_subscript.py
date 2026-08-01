
def infer_parents_subscript(
    subscript_node: nodes.Subscript, ctx: context.InferenceContext | None = None
) -> Iterator[bases.Instance]:
    if isinstance(subscript_node.slice, nodes.Const):
        path_cls = next(_extract_single_node(PATH_TEMPLATE).infer())
        return iter([path_cls.instantiate_class()])

    raise UseInferenceDefault

