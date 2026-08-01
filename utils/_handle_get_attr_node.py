
def _handle_get_attr_node(
    node: torch.fx.Node,
    *,
    owned_graphs: Mapping[str, ir.Function],
    node_name_to_local_functions: dict[str, ir.Function],
) -> None:
    """Handle a get_attr node by assigning the corresponding ONNX function to the node name.

    An example ExportedProgram that has uses get_attr nodes is:

        ExportedProgram:
        class GraphModule(torch.nn.Module):
            def forward(self, arg0_1: "f32[5]"):
                true_graph_0 = self.true_graph_0  # get_attr
                false_graph_0 = self.false_graph_0  # get_attr
                conditional = torch.ops.higher_order.cond(False, true_graph_0, false_graph_0, [arg0_1]);  true_graph_0 = false_graph_0 = arg0_1 = None
                getitem: "f32[5]" = conditional[0];  conditional = None
                return (getitem,)

            class <lambda>(torch.nn.Module):
                def forward(self, arg0_1: "f32[5]"):
                    cos: "f32[5]" = torch.ops.aten.cos.default(arg0_1);  arg0_1 = None
                    return (cos,)

            class <lambda>(torch.nn.Module):
                def forward(self, arg0_1: "f32[5]"):
                    sin: "f32[5]" = torch.ops.aten.sin.default(arg0_1);  arg0_1 = None
                    return (sin,)

    Args:
        node: The FX node to translate.
        owned_graphs: A mapping of subgraph names to the corresponding ONNX functions.
        node_name_to_local_functions: A mapping of local function names to their corresponding ONNX functions.
    """
    if not isinstance(node.target, str):
        logger.warning(
            "Expected node.target for the node %s to be a string, but got '%s'. There may be an internal error.",
            node,
            type(node.target),
        )
        return
    function = owned_graphs[node.target]
    node_name_to_local_functions[node.name] = function

