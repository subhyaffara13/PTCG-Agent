
def has_yield_from_expression(fdef: FuncBase) -> bool:
    seeker = YieldFromSeeker()
    fdef.accept(seeker)
    return seeker.found

