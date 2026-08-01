
def compare(actual, expected, actual_name="actual", expected_name="expected", return_diff=False):
    """Compare two strings, lists or dict-like objects"""
    if actual != expected:
        diff = difflib.unified_diff(
            _multilines(expected),
            _multilines(actual),
            expected_name,
            actual_name,
            lineterm="",
        )
        if expected_name == "" and actual_name == "":
            diff = list(diff)[2:]
        diff = "\n".join(diff)
        if return_diff:
            return diff
        raise AssertionError("\n" + diff)
    return "" if return_diff else None


def compare(before, after, format_flamegraph=format_flamegraph):
    def _seg_key(seg):
        return (seg["address"], seg["total_size"])

    def _seg_info(seg):
        return f"stream_{seg['stream']};seg_{seg['address']}"

    f = io.StringIO()

    before_segs = {_seg_key(seg) for seg in before}
    after_segs = {_seg_key(seg) for seg in after}

    print(f"only_before = {[a for a, _ in (before_segs - after_segs)]}")
    print(f"only_after = {[a for a, _ in (after_segs - before_segs)]}")

    for seg in before:
        if _seg_key(seg) not in after_segs:
            _write_blocks(f, f"only_before;{_seg_info(seg)}", seg["blocks"])

    for seg in after:
        if _seg_key(seg) not in before_segs:
            _write_blocks(f, f"only_after;{_seg_info(seg)}", seg["blocks"])

    return format_flamegraph(f.getvalue())


def compare(a, b, x):
    """Returns "<" if a<b, "=" for a == b, ">" for a>b"""
    # log(exp(...)) must always be simplified here for termination
    la, lb = log(a), log(b)
    if isinstance(a, Basic) and (isinstance(a, exp) or (a.is_Pow and a.base == S.Exp1)):
        la = a.exp
    if isinstance(b, Basic) and (isinstance(b, exp) or (b.is_Pow and b.base == S.Exp1)):
        lb = b.exp

    c = limitinf(la/lb, x)
    if c == 0:
        return "<"
    elif c.is_infinite:
        return ">"
    else:
        return "="


def compare(baseline_results, treatment_results, verbose, rtol=1e-1, atol=1e-3):
    # Validate the output of baseline and treatment, to make sure the results are similar.
    diff_count = 0
    max_abs_diff = 0
    max_diff_percentage = 0
    case_passed = True
    for test_case_id, results in enumerate(baseline_results):
        for i in range(len(results)):
            treatment_output = treatment_results[test_case_id][i]
            abs_diff_tensor = np.abs(treatment_output - results[i])
            abs_diff = np.amax(abs_diff_tensor)
            if verbose and abs_diff > atol:
                print("abs_diff", abs_diff)
                print("treatment", treatment_output)
                print("baseline", results[i])

            count_exceeding = np.sum(abs_diff_tensor > atol)
            total_elements = abs_diff_tensor.size
            percentage_exceeding = (count_exceeding / total_elements) * 100
            max_diff_percentage = max(max_diff_percentage, percentage_exceeding)

            max_abs_diff = max(max_abs_diff, abs_diff)
            if not np.allclose(results[i].tolist(), treatment_output.tolist(), rtol=rtol, atol=atol):
                if case_passed:
                    case_passed = False
                    diff_count += 1

                    if verbose:
                        print(f"case {test_case_id} output {i}")
                        print(f"baseline={results[i].tolist()}\ntreatment={treatment_output}")
                        print(f"abs_diff={abs_diff}")

    if diff_count == 0:
        print(f"100% passed for {len(baseline_results)} random inputs given thresholds (rtol={rtol}, atol={atol}).")
    else:
        print(
            f"WARNING: {diff_count} out of {len(baseline_results)} results NOT passed for thresholds (rtol={rtol}, atol={atol})."
        )

    print(f"maximum absolute difference={max_abs_diff}")
    print(f"maximum percentage of elements that exceeds atol={atol} is {max_diff_percentage:.3f}%")
    return max_abs_diff, case_passed


def compare(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], comparison_direction: _Union[_Any, _ods_ir.Attribute], *, compare_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CompareOp(lhs=lhs, rhs=rhs, comparison_direction=comparison_direction, compare_type=compare_type, results=results, loc=loc, ip=ip).result


def compare(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], comparison_direction: _Union[_Any, _ods_ir.Attribute], *, compare_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CompareOp(lhs=lhs, rhs=rhs, comparison_direction=comparison_direction, compare_type=compare_type, results=results, loc=loc, ip=ip).result

