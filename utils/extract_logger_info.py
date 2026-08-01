
def extract_logger_info(
    model_a: nn.Module,
    model_b: nn.Module,
    logger_cls: Callable,
    model_name_to_use_for_layer_names: str,
) -> NSResultsType:
    """
    Traverse all loggers in `model_a` and `model_b`, and extract the logged
    information.

    Args:
        model_a: model A
        model_b: model B
        logger_cls: class of Logger to use
        model_name_to_use_for_layer_names: string name of model to use for
          layer names in the output

    Return:
        NSResultsType, containing the logged comparisons
    """
    torch._C._log_api_usage_once(
        "quantization_api._numeric_suite_fx.extract_logger_info"
    )
    results: NSResultsType = {}
    for model in (model_a, model_b):
        _extract_logger_info_one_model(model, results, logger_cls)
    # fill in missing fqn entries
    maybe_add_missing_fqns(results)
    # rekey on the name of model b
    results = rekey_logger_info_on_node_name_of_model(
        results, model_name_to_use_for_layer_names
    )
    return results

