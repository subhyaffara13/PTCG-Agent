from typing import Any

def pytest_report_from_serializable(
    config: Config,
    data: dict[str, Any],
) -> CollectReport | TestReport | None:
    """Restore a report object previously serialized with
    :hook:`pytest_report_to_serializable`.

    :param config: The pytest config object.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. The exact details may depend
    on the plugin which calls the hook.
    """


def pytest_report_from_serializable(
    data: dict[str, Any],
) -> CollectReport | TestReport | None:
    if "$report_type" in data:
        if data["$report_type"] == "TestReport":
            return TestReport._from_json(data)
        elif data["$report_type"] == "CollectReport":
            return CollectReport._from_json(data)
        assert False, "Unknown report_type unserialize data: {}".format(
            data["$report_type"]
        )
    return None


def pytest_report_from_serializable(data: dict[str, Any]) -> SubtestReport | None:
    if data.get("_report_type") == "SubTestReport":
        return SubtestReport._from_json(data)
    return None

