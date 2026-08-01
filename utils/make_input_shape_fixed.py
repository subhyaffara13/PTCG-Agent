
def make_input_shape_fixed(graph: onnx.GraphProto, input_name: str, fixed_shape: [int]):
    """
    Update the named graph input to set shape to the provided value. This can be used to set unknown dims as well
    as to replace dim values.
    If setting the input shape replaces a dim_param, update any other values in the graph that use the dim_param.
    :param graph: Graph to update
    :param input_name: Name of graph input to update.
    :param fixed_shape: Shape to use.
    """

    # remove any invalid dim values first. typically this is a dim_value of -1.
    remove_invalid_dim_values(graph)

    for i in graph.input:
        if i.name == input_name:
            if not i.type.HasField("tensor_type"):
                raise ValueError(f"Input {input_name} is not a tensor")

            # graph inputs are required to have a shape to provide the rank
            shape = i.type.tensor_type.shape
            if len(shape.dim) != len(fixed_shape):
                raise ValueError(f"Rank mismatch. Existing:{len(shape.dim)} Replacement:{len(fixed_shape)}")

            for idx, dim in enumerate(shape.dim):
                # check any existing fixed dims match
                if dim.HasField("dim_value"):
                    if dim.dim_value != fixed_shape[idx]:
                        raise ValueError(
                            f"Can't replace existing fixed size of {dim.dim_value} with {fixed_shape[idx]} "
                            f"for dimension {idx + 1}"
                        )
                elif dim.HasField("dim_param"):
                    # replacing a dim_param so have to do that through the entire graph
                    make_dim_param_fixed(graph, dim.dim_param, fixed_shape[idx])
                else:
                    # replacing an unknown dim
                    dim.Clear()
                    dim.dim_value = fixed_shape[idx]

            return

    raise ValueError(
        f"Input {input_name} was not found in graph inputs. "
        f"Valid input names are: {','.join([i.name for i in graph.input])}"
    )

