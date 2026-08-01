
def get_longformer_inputs(onnx_file, input_ids_name=None, input_mask_name=None, global_mask_name=None):
    """
    Get graph inputs for longformer model.
    """
    model = ModelProto()
    with open(onnx_file, "rb") as f:
        model.ParseFromString(f.read())

    onnx_model = OnnxModel(model)
    graph_inputs = onnx_model.get_graph_inputs_excluding_initializers()

    if input_ids_name is not None:
        input_ids = onnx_model.find_graph_input(input_ids_name)
        if input_ids is None:
            raise ValueError(f"Graph does not have input named {input_ids_name}")

        input_mask = None
        if input_mask_name:
            input_mask = onnx_model.find_graph_input(input_mask_name)
            if input_mask is None:
                raise ValueError(f"Graph does not have input named {input_mask_name}")

        global_mask = None
        if global_mask_name:
            global_mask = onnx_model.find_graph_input(global_mask_name)
            if global_mask is None:
                raise ValueError(f"Graph does not have input named {global_mask_name}")

        expected_inputs = 1 + (1 if input_mask else 0) + (1 if global_mask else 0)
        if len(graph_inputs) != expected_inputs:
            raise ValueError(f"Expect the graph to have {expected_inputs} inputs. Got {len(graph_inputs)}")

        return input_ids, input_mask, global_mask

    if len(graph_inputs) != 3:
        raise ValueError(f"Expect the graph to have 3 inputs. Got {len(graph_inputs)}")

    # Try guess the inputs based on naming.
    input_ids = None
    input_mask = None
    global_mask = None
    for input in graph_inputs:
        input_name_lower = input.name.lower()
        if "global" in input_name_lower:
            global_mask = input
        elif "mask" in input_name_lower:
            input_mask = input
        else:
            input_ids = input

    if input_ids and input_mask and global_mask:
        return input_ids, input_mask, global_mask

    raise ValueError("Fail to assign 3 inputs. You might try rename the graph inputs.")

