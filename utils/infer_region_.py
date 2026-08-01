
def inferRegion_(peak):
    """Infer start and end for a (non-intermediate) region

    This helper function computes the applicability region for
    variation tuples whose INTERMEDIATE_REGION flag is not set in the
    TupleVariationHeader structure.  Variation tuples apply only to
    certain regions of the variation space; outside that region, the
    tuple has no effect.  To make the binary encoding more compact,
    TupleVariationHeaders can omit the intermediateStartTuple and
    intermediateEndTuple fields.
    """
    start, end = {}, {}
    for axis, value in peak.items():
        start[axis] = min(value, 0.0)  # -0.3 --> -0.3; 0.7 --> 0.0
        end[axis] = max(value, 0.0)  # -0.3 -->  0.0; 0.7 --> 0.7
    return (start, end)

