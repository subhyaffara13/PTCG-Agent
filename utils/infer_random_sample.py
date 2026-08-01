
def infer_random_sample(node, context: InferenceContext | None = None):
    if len(node.args) != 2:
        raise UseInferenceDefault

    inferred_length = safe_infer(node.args[1], context=context)
    if not isinstance(inferred_length, nodes.Const):
        raise UseInferenceDefault
    if not isinstance(inferred_length.value, int):
        raise UseInferenceDefault

    inferred_sequence = safe_infer(node.args[0], context=context)
    if not inferred_sequence:
        raise UseInferenceDefault

    if not isinstance(inferred_sequence, ACCEPTED_ITERABLES_FOR_SAMPLE):
        raise UseInferenceDefault

    if inferred_length.value > len(inferred_sequence.elts):
        # In this case, this will raise a ValueError
        raise UseInferenceDefault

    try:
        elts = random.sample(inferred_sequence.elts, inferred_length.value)
    except ValueError as exc:
        raise UseInferenceDefault from exc

    new_node = nodes.List(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.scope(),
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    new_elts = [
        _clone_node_with_lineno(elt, parent=new_node, lineno=new_node.lineno)
        for elt in elts
    ]
    new_node.postinit(new_elts)
    return iter((new_node,))

