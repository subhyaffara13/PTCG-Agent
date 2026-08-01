
def text_string_to_metric_families(text: str) -> Iterable[Metric]:
    """Parse Prometheus text format from a unicode string.

    See text_fd_to_metric_families.
    """
    yield from text_fd_to_metric_families(StringIO.StringIO(text))


def text_string_to_metric_families(text):
    """Parse Openmetrics text format from a unicode string.

    See text_fd_to_metric_families.
    """
    yield from text_fd_to_metric_families(StringIO.StringIO(text))

