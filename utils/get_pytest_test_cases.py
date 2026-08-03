from typing import Any

def get_pytest_test_cases(argv: list[str]) -> list[str]:
    class TestCollectorPlugin:
        def __init__(self) -> None:
            self.tests: list[Any] = []

        def pytest_collection_finish(self, session):
            for item in session.items:
                self.tests.append(session.config.cwd_relative_nodeid(item.nodeid))

    test_collector_plugin = TestCollectorPlugin()
    import pytest
    pytest.main(
        [arg for arg in argv if arg != '-vv'] + ['--collect-only', '-qq', '--use-main-module'],
        plugins=[test_collector_plugin]
    )
    return test_collector_plugin.tests

