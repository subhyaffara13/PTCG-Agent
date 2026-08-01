
def infer_numpy_attribute(
    sources: dict[str, str],
    node: nodes.Attribute,
    context: InferenceContext | None = None,
):
    extracted_node = extract_node(sources[node.attrname])
    return extracted_node.infer(context=context)

