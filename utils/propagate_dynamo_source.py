
def propagate_dynamo_source(orig_gm: fx.GraphModule, split_gm: fx.GraphModule) -> None:
    name_to_dynamo_source = {}
    for node in orig_gm.graph.find_nodes(op="placeholder"):
        name_to_dynamo_source[node.name] = node._dynamo_source

    for name, module in split_gm.named_modules():
        if "." not in name and len(name):
            for node in module.graph.find_nodes(op="placeholder"):
                # non-placeholder in original_gm may become placeholder in submodules
                node._dynamo_source = name_to_dynamo_source.get(node.name)

