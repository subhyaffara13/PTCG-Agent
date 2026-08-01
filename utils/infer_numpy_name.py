
def infer_numpy_name(
    sources: dict[str, str], node: nodes.Name, context: InferenceContext | None = None
):
    extracted_node = extract_node(sources[node.name])
    return extracted_node.infer(context=context)

