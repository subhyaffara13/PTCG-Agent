
def raises_chained_assignment_error(extra_warnings=(), extra_match=()):
    from pandas._testing import assert_produces_warning

    if CHAINED_WARNING_DISABLED:
        if not extra_warnings:
            from contextlib import nullcontext

            return nullcontext()
        else:
            return assert_produces_warning(
                extra_warnings,
                match=extra_match,
            )
    else:
        warning = ChainedAssignmentError
        match = (
            "A value is being set on a copy of a DataFrame or Series "
            "through chained assignment"
        )
        if extra_warnings:
            warning = (warning, *extra_warnings)  # type: ignore[assignment]
        return assert_produces_warning(
            warning,
            match=(match, *extra_match),
        )

