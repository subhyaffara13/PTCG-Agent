
def reduce_rational_inequalities_wrap(condition, var):
    if condition.is_Relational:
        return _reduce_inequalities([[condition]], var, relational=False)
    if isinstance(condition, Or):
        return Union(*[_reduce_inequalities([[arg]], var, relational=False)
            for arg in condition.args])
    if isinstance(condition, And):
        intervals = [_reduce_inequalities([[arg]], var, relational=False)
            for arg in condition.args]
        I = intervals[0]
        for i in intervals:
            I = I.intersect(i)
        return I

