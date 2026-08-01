
def _print_comparison_summary(
    stats: ComparisonStats,
    show_repro: int = 0,
) -> None:
    """Print discrepancy details for an operator."""
    # Per aten op variant breakdown
    fp_by_op: dict[str, set[ComboKey]] = defaultdict(set)
    for d in stats.false_positives:
        op_str = str(d.aten_op)
        fp_by_op[op_str].add((d.input_placements, d.output_placements))
    fn_by_op: dict[str, set[ComboKey]] = defaultdict(set)
    for d in stats.false_negatives:
        op_str = str(d.aten_op)
        fn_by_op[op_str].add((d.input_placements, d.output_placements))

    all_ops = sorted(set(stats.true_positives_by_op) | set(fp_by_op) | set(fn_by_op))
    if len(all_ops) > 1:
        for op_str in all_ops:
            tp = stats.true_positives_by_op.get(op_str, 0)
            fp = len(fp_by_op.get(op_str, set()))
            fn = len(fn_by_op.get(op_str, set()))
            print(f"  {op_str}: {tp} correct, {fp} incorrect, {fn} missing")

    _print_discrepancy_section(
        "Incorrect (has rule but ground truth invalid)",
        stats.false_positives,
        show_repro,
    )
    _print_discrepancy_section(
        "Possibly missing (valid in ground truth but no DTensor rule)",
        stats.false_negatives,
        show_repro,
    )

