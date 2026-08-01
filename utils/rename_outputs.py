
def rename_outputs(model: ir.Model, new_names: Sequence[str]) -> None:
    unique_names = frozenset(new_names)
    if len(unique_names) != len(new_names):
        seen = set()
        duplicates = []
        for name in new_names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)
        raise ValueError(f"Output names cannot be duplicated: {duplicates}")

    for output, new_name in zip(model.graph.outputs, new_names):
        output.metadata_props["pkg.torch.onnx.original_node_name"] = str(output.name)
        output.name = new_name

