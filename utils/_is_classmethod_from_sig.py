
def _is_classmethod_from_sig(function: AnyDecoratorCallable) -> bool:
    sig = signature_no_eval(unwrap_wrapped_function(function))
    first = next(iter(sig.parameters.values()), None)
    if first and first.name == 'cls':
        return True
    return False

