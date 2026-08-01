
def rekey_logger_info_on_node_name_of_model(
    results: NSResultsType,
    model_name: str,
) -> NSResultsType:
    """
    Rekeys the layer name of a results dictionary to use node names
    from `model_name`.

    For example, transforms

        {'base_op_1_0': {'node_output': {'model_a':
          [{'ref_node_name': 'linear1', ...}]}}}

    into

        {'linear1': {'node_output': {'model_a':
          [{'ref_node_name': 'linear1', ...}]}}}

    Note: we cannot use these node names directly because they are not
    guaranteed to be consistent across models. This is why we extract
    the results first and rekey afterwards.
    """
    new_results = {}
    for old_layer_name, result_type_to_results in results.items():
        new_layer_name = None
        for model_name_to_results in result_type_to_results.values():
            for cur_model_name, list_of_results in model_name_to_results.items():
                if cur_model_name == model_name:
                    if len(list_of_results) == 0:
                        raise AssertionError("Expected list_of_results to be not empty")
                    new_layer_name = list_of_results[0]["ref_node_name"]
                else:
                    continue
        if new_layer_name is not None:
            new_results[new_layer_name] = result_type_to_results
        else:
            new_results[old_layer_name] = result_type_to_results
    return new_results

