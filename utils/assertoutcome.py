
def assertoutcome(
    outcomes: tuple[
        Sequence[TestReport],
        Sequence[CollectReport | TestReport],
        Sequence[CollectReport | TestReport],
    ],
    passed: int = 0,
    skipped: int = 0,
    failed: int = 0,
) -> None:
    __tracebackhide__ = True

    realpassed, realskipped, realfailed = outcomes
    obtained = {
        "failed": len(realfailed),
        "passed": len(realpassed),
        "skipped": len(realskipped),
    }
    expected = {"failed": failed, "passed": passed, "skipped": skipped}
    assert obtained == expected, outcomes

