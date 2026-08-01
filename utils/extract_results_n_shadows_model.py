
def extract_results_n_shadows_model(model: torch.nn.Module) -> NSResultsType:
    """
    Extracts logger results from `model`.
    """
    results: NSResultsType = {}
    _extract_logger_info_one_model(model, results, OutputLogger)
    return results

