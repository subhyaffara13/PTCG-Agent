
def create_results_comparison(
    results_grouped,
) -> Any:
    """
    Input:

    {
      'subgraph_0': {
        '0': {
          'ref_node_name': '...',
          'ref_node_target_type': ...,
          'values': [torch.tensor(...), ...],
          'qconfig_str': '',
          'comparisons': [],
          'comparison_fn_name': '',
          'fqn': '...',
        },
        '1': {
          'ref_node_name': '...',
          'ref_node_target_type': ...,
          'values': [torch.tensor(...), ...],
          'qconfig_str': '...',
          'comparisons': [torch.tensor(...), ...],
          'comparison_fn_name': 'sqnr',
          'fqn': '...',
        },
      },
    }

    Output:
    {
      'subgraph_0': {
        'ref_node_name': '...',
        'ref_node_target_type': '...',
        'fqn': '...',
        'candidates': {
          '1': {
            'qconfig_str': ...,
            'comparison_fn_name': 'sqnr',
            'cmp_raw': [..., ...],
            'cmp_mean': ...,
          },
          ...,
        },
      },
    }
    """

    results_comparison = {}

    for subgraph_name, subgraph_results in results_grouped.items():
        candidates = {}
        for subgraph_inner_name, subgraph_inner_result in subgraph_results.items():
            # skip comparing baseline to baseline
            if subgraph_inner_name == "0":
                continue

            # we expect the comparisons to be precalculated from
            # calibration, so we just fetch them here
            cmp_raw = subgraph_inner_result["comparisons"]
            cmp_raw_tensor = torch.stack(cmp_raw)

            candidates[subgraph_inner_name] = {
                "qconfig_str": subgraph_inner_result["qconfig_str"],
                "comparison_fn_name": subgraph_inner_result["comparison_fn_name"],
                "cmp_raw": cmp_raw_tensor,
                "cmp_mean": torch.mean(cmp_raw_tensor),
            }

        results_comparison[subgraph_name] = {
            "ref_node_name": subgraph_results["0"]["ref_node_name"],
            "ref_node_target_type": subgraph_results["0"]["ref_node_target_type"],
            "fqn": subgraph_results["0"]["fqn"],
            "candidates": candidates,
        }

    return results_comparison

