
def use_derived(fn: NativeFunctionWithDifferentiabilityInfo) -> bool:
    f = fn.func
    name = cpp.name(f.func)
    return name not in MANUAL_AUTOGRAD and dispatch_strategy(fn) == "use_derived"

