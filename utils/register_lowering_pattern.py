
def register_lowering_pattern(
    pattern: PatternExpr,
    extra_check: Callable[[Match], bool] = _return_true,
    *,
    pass_dict: _PassDictsType,
    prepend: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Register an aten to inductor IR replacement pattern.  The decorated
    function is saved and then called a lowering time allowing direct
    pattern to inductor IR conversion.
    """

    def decorator(handler: Callable[..., Any]) -> Callable[..., Any]:
        assert callable(handler)
        LoweringPatternEntry(
            pattern=pattern, extra_check=extra_check, handler=handler
        ).register(pass_dict, prepend=prepend)
        handler._inductor_lowering_function = True  # type: ignore[attr-defined]
        return handler

    return decorator


def register_lowering_pattern(
    pattern, extra_check=_return_true, pass_number=1
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """
    Register an aten to inductor IR replacement pattern
    """
    return pattern_matcher.register_lowering_pattern(
        pattern,
        extra_check,
        # pyrefly: ignore [bad-argument-type]
        pass_dict=pass_patterns[pass_number],
    )

