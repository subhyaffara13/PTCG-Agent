
def invoke_quant_tracer(subgraph_fn: ir.Subgraph, *operands, scheme=None):
    output = None
    quant_options = V.graph.current_node.meta.get("quant_options", None)
    assert quant_options is not None

    for i, node in enumerate(subgraph_fn.graph_module.graph.nodes):
        if node.op == "placeholder":
            V.graph.env[node] = operands[i]
            continue
        # todo getattr
        elif node.op == "output":
            args, kwargs = V.graph.fetch_args_kwargs_from_env(node)

            for v in itertools.chain(args, kwargs.values()):
                v.realize()

                if quant_options.codegen_low_precision:
                    V.graph.low_precision_codegen_ops.add(v.get_operation_name())

                V.graph.invoke_quant_ops.add(v.get_operation_name())

            output = torch.fx.Interpreter.output(V.graph, node, args, kwargs)
        else:
            V.graph.env[node] = V.graph.run_node(node)

    return output

