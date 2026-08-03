from typing import Any

def _apply_constraint(  # noqa: C901
    s: cs.CoreSchema | None, constraint: _ConstraintAnnotation
) -> cs.CoreSchema:
    """Apply a single constraint to a schema."""
    if isinstance(constraint, annotated_types.Gt):
        gt = constraint.gt
        if s and s['type'] in {'int', 'float', 'decimal'}:
            s = s.copy()
            if s['type'] == 'int' and isinstance(gt, int):
                s['gt'] = gt
            elif s['type'] == 'float' and isinstance(gt, float):
                s['gt'] = gt
            elif s['type'] == 'decimal' and isinstance(gt, Decimal):
                s['gt'] = gt
        else:

            def check_gt(v: Any) -> bool:
                return v > gt

            s = _check_func(check_gt, f'> {gt}', s)
    elif isinstance(constraint, annotated_types.Ge):
        ge = constraint.ge
        if s and s['type'] in {'int', 'float', 'decimal'}:
            s = s.copy()
            if s['type'] == 'int' and isinstance(ge, int):
                s['ge'] = ge
            elif s['type'] == 'float' and isinstance(ge, float):
                s['ge'] = ge
            elif s['type'] == 'decimal' and isinstance(ge, Decimal):
                s['ge'] = ge

        def check_ge(v: Any) -> bool:
            return v >= ge

        s = _check_func(check_ge, f'>= {ge}', s)
    elif isinstance(constraint, annotated_types.Lt):
        lt = constraint.lt
        if s and s['type'] in {'int', 'float', 'decimal'}:
            s = s.copy()
            if s['type'] == 'int' and isinstance(lt, int):
                s['lt'] = lt
            elif s['type'] == 'float' and isinstance(lt, float):
                s['lt'] = lt
            elif s['type'] == 'decimal' and isinstance(lt, Decimal):
                s['lt'] = lt

        def check_lt(v: Any) -> bool:
            return v < lt

        s = _check_func(check_lt, f'< {lt}', s)
    elif isinstance(constraint, annotated_types.Le):
        le = constraint.le
        if s and s['type'] in {'int', 'float', 'decimal'}:
            s = s.copy()
            if s['type'] == 'int' and isinstance(le, int):
                s['le'] = le
            elif s['type'] == 'float' and isinstance(le, float):
                s['le'] = le
            elif s['type'] == 'decimal' and isinstance(le, Decimal):
                s['le'] = le

        def check_le(v: Any) -> bool:
            return v <= le

        s = _check_func(check_le, f'<= {le}', s)
    elif isinstance(constraint, annotated_types.Len):
        min_len = constraint.min_length
        max_len = constraint.max_length

        if s and s['type'] in {'str', 'list', 'tuple', 'set', 'frozenset', 'dict'}:
            assert (
                s['type'] == 'str'
                or s['type'] == 'list'
                or s['type'] == 'tuple'
                or s['type'] == 'set'
                or s['type'] == 'dict'
                or s['type'] == 'frozenset'
            )
            s = s.copy()
            if min_len != 0:
                s['min_length'] = min_len
            if max_len is not None:
                s['max_length'] = max_len

        def check_len(v: Any) -> bool:
            if max_len is not None:
                return (min_len <= len(v)) and (len(v) <= max_len)
            return min_len <= len(v)

        s = _check_func(check_len, f'length >= {min_len} and length <= {max_len}', s)
    elif isinstance(constraint, annotated_types.MultipleOf):
        multiple_of = constraint.multiple_of
        if s and s['type'] in {'int', 'float', 'decimal'}:
            s = s.copy()
            if s['type'] == 'int' and isinstance(multiple_of, int):
                s['multiple_of'] = multiple_of
            elif s['type'] == 'float' and isinstance(multiple_of, float):
                s['multiple_of'] = multiple_of
            elif s['type'] == 'decimal' and isinstance(multiple_of, Decimal):
                s['multiple_of'] = multiple_of

        def check_multiple_of(v: Any) -> bool:
            return v % multiple_of == 0

        s = _check_func(check_multiple_of, f'% {multiple_of} == 0', s)
    elif isinstance(constraint, annotated_types.Timezone):
        tz = constraint.tz

        if tz is ...:
            if s and s['type'] == 'datetime':
                s = s.copy()
                s['tz_constraint'] = 'aware'
            else:

                def check_tz_aware(v: object) -> bool:
                    assert isinstance(v, datetime.datetime)
                    return v.tzinfo is not None

                s = _check_func(check_tz_aware, 'timezone aware', s)
        elif tz is None:
            if s and s['type'] == 'datetime':
                s = s.copy()
                s['tz_constraint'] = 'naive'
            else:

                def check_tz_naive(v: object) -> bool:
                    assert isinstance(v, datetime.datetime)
                    return v.tzinfo is None

                s = _check_func(check_tz_naive, 'timezone naive', s)
        else:
            raise NotImplementedError('Constraining to a specific timezone is not yet supported')
    elif isinstance(constraint, annotated_types.Interval):
        if constraint.ge:
            s = _apply_constraint(s, annotated_types.Ge(constraint.ge))
        if constraint.gt:
            s = _apply_constraint(s, annotated_types.Gt(constraint.gt))
        if constraint.le:
            s = _apply_constraint(s, annotated_types.Le(constraint.le))
        if constraint.lt:
            s = _apply_constraint(s, annotated_types.Lt(constraint.lt))
        assert s is not None
    elif isinstance(constraint, annotated_types.Predicate):
        func = constraint.func
        # Same logic as in `_known_annotated_metadata.apply_known_metadata()`:
        predicate_name = f'{func.__qualname__!r} ' if hasattr(func, '__qualname__') else ''

        def predicate_func(v: Any) -> Any:
            if not func(v):
                raise PydanticCustomError(
                    'predicate_failed',
                    f'Predicate {predicate_name}failed',  # pyright: ignore[reportArgumentType]
                )
            return v

        if s is None:
            s = cs.no_info_plain_validator_function(predicate_func)
        else:
            s = cs.no_info_after_validator_function(predicate_func, s)
    elif isinstance(constraint, _NotEq):
        value = constraint.value

        def check_not_eq(v: Any) -> bool:
            return operator.__ne__(v, value)

        s = _check_func(check_not_eq, f'!= {value}', s)
    elif isinstance(constraint, _Eq):
        value = constraint.value

        def check_eq(v: Any) -> bool:
            return operator.__eq__(v, value)

        s = _check_func(check_eq, f'== {value}', s)
    elif isinstance(constraint, _In):
        values = constraint.values

        def check_in(v: Any) -> bool:
            return operator.__contains__(values, v)

        s = _check_func(check_in, f'in {values}', s)
    elif isinstance(constraint, _NotIn):
        values = constraint.values

        def check_not_in(v: Any) -> bool:
            return operator.__not__(operator.__contains__(values, v))

        s = _check_func(check_not_in, f'not in {values}', s)
    else:
        assert isinstance(constraint, Pattern)
        if s and s['type'] == 'str':
            s = s.copy()
            s['pattern'] = constraint.pattern
        else:

            def check_pattern(v: object) -> bool:
                assert isinstance(v, str)
                return constraint.match(v) is not None

            s = _check_func(check_pattern, f'~ {constraint.pattern}', s)
    return s

