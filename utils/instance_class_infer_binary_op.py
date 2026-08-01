
def instance_class_infer_binary_op(
    self: nodes.ClassDef,
    opnode: nodes.AugAssign | nodes.BinOp,
    operator: str,
    other: InferenceResult,
    context: InferenceContext,
    method: SuccessfulInferenceResult,
) -> Generator[InferenceResult]:
    return method.infer_call_result(self, context)

