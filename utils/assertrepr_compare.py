
def assertrepr_compare(
    op: str,
    left: object,
    right: object,
    *,
    verbose: int,
    highlighter: _HighlightFunc,
    assertion_text_diff_style: _AssertionTextDiffStyle,
) -> Iterator[str]:
    """Yield specialised explanations for some operators/operands.

    The first line yielded is always the summary (``left op right``);
    subsequent lines are the detailed explanation. Yields nothing when no
    specialised explanation applies, which lets consumers map an empty
    iterator to "no explanation" without materialising anything.

    The iterator is lazy on purpose: a streaming consumer can stop pulling
    lines as soon as it has enough to show, so an enormous diff doesn't
    have to be built in full just to be thrown away.
    """
    # Strings which normalize equal are often hard to distinguish when printed; use ascii() to make this easier.
    # See issue #3246.
    use_ascii = (
        isinstance(left, str)
        and isinstance(right, str)
        and normalize("NFD", left) == normalize("NFD", right)
    )

    if verbose > 1:
        left_repr = saferepr_unlimited(left, use_ascii=use_ascii)
        right_repr = saferepr_unlimited(right, use_ascii=use_ascii)
    else:
        # XXX: "15 chars indentation" is wrong
        #      ("E       AssertionError: assert "); should use term width.
        maxsize = (
            80 - 15 - len(op) - 2
        ) // 2  # 15 chars indentation, 1 space around op

        left_repr = saferepr(left, maxsize=maxsize, use_ascii=use_ascii)
        right_repr = saferepr(right, maxsize=maxsize, use_ascii=use_ascii)

    summary = f"{left_repr} {op} {right_repr}"

    try:
        if op == "==":
            source = _compare_eq_any(
                left,
                right,
                highlighter,
                verbose,
                assertion_text_diff_style,
            )
        elif op == "not in" and istext(left) and istext(right):
            source = _notin_text(left, right, verbose)
        elif op in {"!=", ">=", "<=", ">", "<"} and isset(left) and isset(right):
            source = SET_COMPARISON_FUNCTIONS[op](left, right, highlighter, verbose)
        else:
            source = iter(())

        # Only yield the summary if there is a detailed explanation.
        # Make sure there's a separating empty line after the summary.
        summary_yielded = False
        for line in source:
            if not summary_yielded:
                yield summary
                if line != "":
                    yield ""
                summary_yielded = True
            yield line
    except outcomes.Exit:
        raise
    except Exception:
        repr_crash = _pytest._code.ExceptionInfo.from_current()._getreprcrash()
        if not summary_yielded:
            yield summary
            yield ""
            summary_yielded = True
        yield (
            f"(pytest_assertion plugin: representation of details failed: {repr_crash}."
        )
        yield " Probably an object has a faulty __repr__.)"

