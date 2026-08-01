
def infer_statistics_quantiles(
    node: nodes.Call, context: InferenceContext | None = None
) -> Iterator[InferenceResult]:
    """Infer the result of statistics.quantiles() calls.

    Returns Uninferable because quantiles() has complex runtime behavior
    that cannot be statically analyzed, preventing false positives in
    pylint's unbalanced-tuple-unpacking checker.

    statistics.quantiles() returns a list with (n-1) elements, but static
    analysis sees only the empty list initializations in the function body.
    """
    yield Uninferable

