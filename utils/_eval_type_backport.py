
def _eval_type_backport(
    value: Any,
    globalns: GlobalsNamespace | None = None,
    localns: MappingNamespace | None = None,
    type_params: tuple[Any, ...] | None = None,
) -> Any:
    try:
        return _eval_type(value, globalns, localns, type_params)
    except TypeError as e:
        if not (isinstance(value, typing.ForwardRef) and is_backport_fixable_error(e)):
            raise

        try:
            from eval_type_backport import eval_type_backport
        except ImportError:
            raise TypeError(
                f'Unable to evaluate type annotation {value.__forward_arg__!r}. If you are making use '
                'of the new typing syntax (unions using `|` since Python 3.10 or builtins subscripting '
                'since Python 3.9), you should either replace the use of new syntax with the existing '
                '`typing` constructs or install the `eval_type_backport` package.'
            ) from e

        return eval_type_backport(
            value,
            globalns,
            localns,  # pyright: ignore[reportArgumentType], waiting on a new `eval_type_backport` release.
            try_default=False,
        )

