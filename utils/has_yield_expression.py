
def has_yield_expression(fdef: FuncBase) -> bool:
    seeker = YieldSeeker()
    fdef.accept(seeker)
    return seeker.found

