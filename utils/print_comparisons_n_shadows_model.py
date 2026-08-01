
def print_comparisons_n_shadows_model(results: NSResultsType) -> None:
    """
    Prints a summary of extracted `results`.
    """
    results_grouped = group_results_by_subgraph(results)
    results_comparison = create_results_comparison(results_grouped)
    print_n_shadows_summary(results_comparison)

