
def _set_input_and_output_names(graph, input_names, output_names) -> None:
    def set_names(node_list, name_list, descriptor) -> None:
        if name_list is None:
            return
        if len(name_list) > len(node_list):
            raise RuntimeError(
                f"number of {descriptor} names provided ({len(name_list)}) "
                f"exceeded number of {descriptor}s ({len(node_list)})"
            )

        # Mark if the output node DebugName is set before.
        output_node_set = set()
        for i, (name, node) in enumerate(zip(name_list, node_list)):
            # Duplicated output node, insert onnx::Identity to avoid setting the same DebugName after setDebugName().
            if descriptor == "output":
                if node in output_node_set:
                    identity_node = graph.create("onnx::Identity")
                    identity_node.insertAfter(node.node())
                    identity_node.addInput(node)
                    identity_node.output().setType(node.type())
                    graph.return_node().replaceInput(i, identity_node.output())
                    node = identity_node.output()
                output_node_set.add(node)

            if node.debugName() != name:
                node.setDebugName(name)

    set_names(list(graph.inputs()), input_names, "input")
    set_names(list(graph.outputs()), output_names, "output")

