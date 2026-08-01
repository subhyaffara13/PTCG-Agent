
def _format_exceptions_for_all_strategies(
    results: list[_capture_strategies.Result],
) -> str:
    """Format all the exceptions from the capture strategies."""
    return "\n".join(
        [
            f"# ⚠️ Errors from strategy '{result.strategy}': -----------------------\n\n"
            f"{_format_exception(result.exception)}\n"
            for result in results
            if result.exception is not None
        ]
    )

