
def _infer_last(
    arg: SuccessfulInferenceResult, context: InferenceContext
) -> InferenceResult:
    res = util.Uninferable
    for b in arg.infer(context=context.clone()):
        res = b
    return res

