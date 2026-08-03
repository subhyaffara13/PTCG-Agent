import logging

def check_shapes(graph: onnx.GraphProto, logger: logging.Logger | None = None):
    """
    Check the shapes of graph inputs, values and graph outputs to determine if they have static or dynamic sizes.
    NNAPI does not support dynamically sized values. CoreML does, but it will most likely cost performance.
    :param graph: Graph to check. If shape inferencing has been run the checks on values will be meaningful.
    :param logger: Optional logger for diagnostic information.
    :return: Tuple of List of inputs with dynamic shapes, Number of dynamic values found
    """

    # it's OK if the input is dynamically sized and we do a Resize early to a fixed size.
    # it's not good if lots of ops have dynamic inputs

    num_fixed_values = 0
    num_dynamic_values = 0

    dynamic_inputs = []
    for i in graph.input:
        if not is_fixed_size_tensor(i):
            dynamic_inputs.append(i)
            # split/join to remove repeated whitespace and newlines from str(i)
            if logger:
                logger.info(f"Input is not a fixed size tensor: {' '.join(str(i).split())}")
            num_dynamic_values += 1
        else:
            num_fixed_values += 1

    dynamic_outputs = []
    for o in graph.output:
        if not is_fixed_size_tensor(o):
            dynamic_outputs.append(o)
            if logger:
                logger.info(f"Output is not a fixed size tensor: {' '.join(str(o).split())}")
            num_dynamic_values += 1
        else:
            num_fixed_values += 1

    # check we have value info.
    # special case some test graphs with a single node which only have graph input and output values, and
    # a model where all inputs are dynamic (results in no value_info)
    if not graph.value_info and not (len(graph.node) == 1 or len(dynamic_inputs) == len(graph.input)):
        logger.warning(
            "Unable to check shapes within model. ONNX shape inferencing should be run on the model prior to checking."
        )

    for vi in graph.value_info:
        if is_fixed_size_tensor(vi):
            num_fixed_values += 1
        else:
            num_dynamic_values += 1

    if logger:
        logger.info(
            f"Num values with fixed shape={num_fixed_values}. Num values with dynamic shape={num_dynamic_values}"
        )

        if dynamic_inputs:
            if dynamic_outputs:
                logger.info(
                    "Model has dynamic inputs and outputs. Consider re-exporting model with fixed sizes "
                    "if NNAPI or CoreML can be used with this model."
                )
            else:
                logger.info(
                    """Model has dynamically sized inputs but fixed sized outputs.
                       If the sizes become fixed early in the model (e.g. pre-processing of a dynamic input size
                       results in a fixed input size for the majority of the model) performance with NNAPI and CoreML,
                       if applicable, should not be significantly impacted."""
                )

    return dynamic_inputs, num_dynamic_values

