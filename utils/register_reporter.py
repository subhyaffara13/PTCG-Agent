
def register_reporter(
    report_name: str,
    reporter: Callable[[Reports, str], AbstractReporter],
    needs_lxml: bool = False,
) -> None:
    reporter_classes[report_name] = (reporter, needs_lxml)

