
def _infer_method_result_truth(
    instance: Instance, method_name: str, context: InferenceContext
) -> bool | UninferableBase:
    # Get the method from the instance and try to infer
    # its return's truth value.
    meth = next(instance.igetattr(method_name, context=context), None)
    if meth and hasattr(meth, "infer_call_result"):
        if not meth.callable():
            return Uninferable
        try:
            context.callcontext = CallContext(args=[], callee=meth)
            for value in meth.infer_call_result(instance, context=context):
                if isinstance(value, UninferableBase):
                    return value
                try:
                    inferred = next(value.infer(context=context))
                except StopIteration as e:
                    raise InferenceError(context=context) from e
                return inferred.bool_value()
        except InferenceError:
            pass
    return Uninferable

