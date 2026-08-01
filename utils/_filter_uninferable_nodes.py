
def _filter_uninferable_nodes(
    elts: Sequence[InferenceResult], context: InferenceContext
) -> Iterator[SuccessfulInferenceResult]:
    for elt in elts:
        if isinstance(elt, util.UninferableBase):
            yield node_classes.UNATTACHED_UNKNOWN
        else:
            for inferred in elt.infer(context):
                if not isinstance(inferred, util.UninferableBase):
                    yield inferred
                else:
                    yield node_classes.UNATTACHED_UNKNOWN

