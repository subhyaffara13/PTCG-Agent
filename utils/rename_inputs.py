
def rename_inputs(model: ir.Model, new_names: Sequence[str]) -> None:
    unique_names = frozenset(new_names)
    if len(unique_names) != len(new_names):
        seen = set()
        duplicates = []
        for name in new_names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)
        raise ValueError(f"Input names cannot be duplicated: {duplicates}")

    for input, new_name in zip(model.graph.inputs, new_names):
        input.metadata_props["pkg.torch.onnx.original_node_name"] = str(input.name)
        input.name = new_name

