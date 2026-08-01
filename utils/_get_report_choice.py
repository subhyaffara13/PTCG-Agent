
def _get_report_choice(key: str) -> int:
    """Return the actual `doctest` module flag value.

    We want to do it as late as possible to avoid importing `doctest` and all
    its dependencies when parsing options, as it adds overhead and breaks tests.
    """
    import doctest

    return {
        DOCTEST_REPORT_CHOICE_UDIFF: doctest.REPORT_UDIFF,
        DOCTEST_REPORT_CHOICE_CDIFF: doctest.REPORT_CDIFF,
        DOCTEST_REPORT_CHOICE_NDIFF: doctest.REPORT_NDIFF,
        DOCTEST_REPORT_CHOICE_ONLY_FIRST_FAILURE: doctest.REPORT_ONLY_FIRST_FAILURE,
        DOCTEST_REPORT_CHOICE_NONE: 0,
    }[key]

