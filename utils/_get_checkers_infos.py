from typing import Any

def _get_checkers_infos(linter: PyLinter) -> dict[str, dict[str, Any]]:
    """Get info from a checker and handle KeyError."""
    by_checker: dict[str, dict[str, Any]] = {}
    for checker in linter.get_checkers():
        name = checker.name
        if name != MAIN_CHECKER_NAME:
            try:
                by_checker[name]["checker"] = checker
                by_checker[name]["options"] += checker._options_and_values()
                by_checker[name]["msgs"].update(checker.msgs)
                by_checker[name]["reports"] += checker.reports
            except KeyError:
                by_checker[name] = {
                    "checker": checker,
                    "options": list(checker._options_and_values()),
                    "msgs": dict(checker.msgs),
                    "reports": list(checker.reports),
                }
    return by_checker

