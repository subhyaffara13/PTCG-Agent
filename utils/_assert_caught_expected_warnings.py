import re

def _assert_caught_expected_warnings(
    *,
    caught_warnings: Sequence[warnings.WarningMessage],
    expected_warning: type[Warning] | tuple[type[Warning], ...],
    match: str | None,
    check_stacklevel: bool,
) -> None:
    """Assert that there was the expected warning among the caught warnings."""
    saw_warning = False
    matched_message = False
    unmatched_messages = []
    warning_name = (
        tuple(x.__name__ for x in expected_warning)
        if isinstance(expected_warning, tuple)
        else expected_warning.__name__
    )

    for actual_warning in caught_warnings:
        if issubclass(actual_warning.category, expected_warning):
            saw_warning = True

            if check_stacklevel:
                _assert_raised_with_correct_stacklevel(actual_warning)

            if match is not None:
                if re.search(match, str(actual_warning.message)):
                    matched_message = True
                else:
                    unmatched_messages.append(actual_warning.message)

    if not saw_warning:
        raise AssertionError(f"Did not see expected warning of class {warning_name!r}")

    if match and not matched_message:
        raise AssertionError(
            f"Did not see warning {warning_name!r} "
            f"matching '{match}'. The emitted warning messages are "
            f"{unmatched_messages}"
        )

