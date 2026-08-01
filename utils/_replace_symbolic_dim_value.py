
def _replace_symbolic_dim_value(graph: onnx.GraphProto, **kwargs):
    param_to_replace = kwargs["dim_param"]
    value = kwargs["value"]

    def update_dim_values(value_infos):
        for vi in value_infos:
            if vi.type.HasField("tensor_type"):
                shape = vi.type.tensor_type.shape
                if shape:
                    for dim in shape.dim:
                        if dim.HasField("dim_param") and dim.dim_param == param_to_replace:
                            dim.Clear()
                            dim.dim_value = value

    update_dim_values(graph.input)
    update_dim_values(graph.output)
    update_dim_values(graph.value_info)

