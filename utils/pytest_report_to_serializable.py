
def pytest_report_to_serializable(
    config: Config,
    report: CollectReport | TestReport,
) -> dict[str, Any] | None:
    """Serialize the given report object into a data structure suitable for
    sending over the wire, e.g. converted to JSON.

    :param config: The pytest config object.
    :param report: The report.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. The exact details may depend
    on the plugin which calls the hook.
    """


def pytest_report_to_serializable(
    report: CollectReport | TestReport,
) -> dict[str, Any] | None:
    if isinstance(report, TestReport | CollectReport):
        data = report._to_json()
        data["$report_type"] = report.__class__.__name__
        return data
    # TODO: Check if this is actually reachable.
    return None  # type: ignore[unreachable]


def pytest_report_to_serializable(report: TestReport) -> dict[str, Any] | None:
    if isinstance(report, SubtestReport):
        return report._to_json()
    return None

