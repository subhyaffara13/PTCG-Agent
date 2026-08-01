
def print_n_shadows_summary(
    results_comparison,
) -> None:
    """
    Input:

    {
      'subgraph_0': {
        'ref_node_name': 'linear1',
        'ref_node_target_type': '...',
        'fqn': '...',
        'candidates': {
          '1': {
            'qconfig_str': ...,
            'comparison_fn_name': ...,
            'cmp_raw': [45.0, 55.0],
            'cmp_mean': 50.0,
          },
          ...,
        },
      },
    }

    Prints:

    node_name | node_type | fqn | 0    | 1    | ...
    linear1   | ...       | ... | 45.0 | 50.0 | ...
    """

    try:
        from tabulate import tabulate
    except ImportError:
        print(
            "`print_tabular` relies on the library `tabulate`, "
            "which could not be found on this machine. Run `pip "
            "install tabulate` to install the library."
        )
        return

    results = []
    for subgraph_data in results_comparison.values():
        mean_all_candidates = [
            candidate["cmp_mean"]
            for candidate_name, candidate in subgraph_data["candidates"].items()
        ]

        data_row = [
            subgraph_data["ref_node_name"],
            subgraph_data["ref_node_target_type"],
            subgraph_data["fqn"],
            *mean_all_candidates,
        ]
        results.append(data_row)

    max_candidate_idx_len = -1
    for data_row in results:
        max_candidate_idx_len = max(max_candidate_idx_len, len(data_row[1]))
    candidate_idx_headers = [str(x) for x in range(max_candidate_idx_len)]

    headers = ["node_name", "node_type", "fqn", *candidate_idx_headers]
    print(tabulate(results, headers=headers))

