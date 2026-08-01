
def _remove_invalid_dim_values_impl(graph: onnx.GraphProto):
    def clear_invalid_values(value):
        if value.type.HasField("tensor_type"):
            shape = value.type.tensor_type.shape
            if shape:
                for dim in shape.dim:
                    if dim.HasField("dim_value") and dim.dim_value < 1:
                        dim.Clear()

    for i in graph.input:
        clear_invalid_values(i)

    for o in graph.output:
        clear_invalid_values(o)

    for vi in graph.value_info:
        clear_invalid_values(vi)

