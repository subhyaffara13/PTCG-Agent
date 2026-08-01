
def get_results() -> tuple[str, str, str, float]:
    r"""Return all TunableOp results."""
    return torch._C._cuda_tunableop_get_results()  # type: ignore[attr-defined]


def get_results(params, Z, n_jobs=1, compute_mp=True):
    """Batch compute results for multiple parameter and argument values.

    Parameters
    ----------
    params : iterable
        iterable of tuples of floats (a, b, c) specifying parameter values
        a, b, c for hyp2f1
    Z : iterable of complex
        Arguments at which to evaluate hyp2f1
    n_jobs : Optional[int]
        Number of jobs for parallel execution.

    Returns
    -------
    list
        List of tuples of results values. See return value in source code
        of `get_result`.
    """
    input_ = (
        (a, b, c, z, group) for (a, b, c, group), z in product(params, Z)
    )

    with Pool(n_jobs) as pool:
        rows = pool.starmap(
            get_result if compute_mp else get_result_no_mp,
            input_
        )
    return rows


def get_results(manager, sev_level, conf_level, lines):
    bits = []
    issues = manager.get_issue_list(sev_level, conf_level)
    baseline = not isinstance(issues, list)
    candidate_indent = " " * 10

    if not len(issues):
        return "\tNo issues identified."

    for issue in issues:
        # if not a baseline or only one candidate we know the issue
        if not baseline or len(issues[issue]) == 1:
            bits.append(_output_issue_str(issue, "", lines=lines))

        # otherwise show the finding and the candidates
        else:
            bits.append(
                _output_issue_str(
                    issue, "", show_lineno=False, show_code=False
                )
            )

            bits.append("\n-- Candidate Issues --")
            for candidate in issues[issue]:
                bits.append(
                    _output_issue_str(candidate, candidate_indent, lines=lines)
                )
                bits.append("\n")
        bits.append("-" * 50)

    return "\n".join([bit for bit in bits])


def get_results(manager, sev_level, conf_level, lines):
    bits = []
    issues = manager.get_issue_list(sev_level, conf_level)
    baseline = not isinstance(issues, list)
    candidate_indent = " " * 10

    if not len(issues):
        return "\tNo issues identified."

    for issue in issues:
        # if not a baseline or only one candidate we know the issue
        if not baseline or len(issues[issue]) == 1:
            bits.append(_output_issue_str(issue, "", lines=lines))

        # otherwise show the finding and the candidates
        else:
            bits.append(
                _output_issue_str(
                    issue, "", show_lineno=False, show_code=False
                )
            )

            bits.append("\n-- Candidate Issues --")
            for candidate in issues[issue]:
                bits.append(
                    _output_issue_str(candidate, candidate_indent, lines=lines)
                )
                bits.append("\n")
        bits.append("-" * 50)
    return "\n".join([bit for bit in bits])

