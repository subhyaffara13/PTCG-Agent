
def condition(
    cond: Callable[[_T], bool], rule: Callable[[_T], _T]
) -> Callable[[_T], _T]:
    """ Only apply rule if condition is true """
    def conditioned_rl(expr: _T) -> _T:
        if cond(expr):
            return rule(expr)
        return expr
    return conditioned_rl


def condition(cond, brule):
    """ Only apply branching rule if condition is true """
    def conditioned_brl(expr):
        if cond(expr):
            yield from brule(expr)
        else:
            pass
    return conditioned_brl


def condition(condition: _ods_ir.Value[_ods_ir.IntegerType], args: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ConditionOp:
  return ConditionOp(condition=condition, args=args, loc=loc, ip=ip)

