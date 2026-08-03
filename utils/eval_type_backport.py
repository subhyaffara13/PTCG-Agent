import sys
from typing import Any

def eval_type_backport(
    value: Any,
    globalns: GlobalsNamespace | None = None,
    localns: MappingNamespace | None = None,
    type_params: tuple[Any, ...] | None = None,
) -> Any:
    """An enhanced version of `typing._eval_type` which will fall back to using the `eval_type_backport`
    package if it's installed to let older Python versions use newer typing constructs.

    Specifically, this transforms `X | Y` into `typing.Union[X, Y]` and `list[X]` into `typing.List[X]`
    (as well as all the types made generic in PEP 585) if the original syntax is not supported in the
    current Python version.

    This function will also display a helpful error if the value passed fails to evaluate.
    """
    try:
        return _eval_type_backport(value, globalns, localns, type_params)
    except TypeError as e:
        if 'Unable to evaluate type annotation' in str(e):
            raise

        # If it is a `TypeError` and value isn't a `ForwardRef`, it would have failed during annotation definition.
        # Thus we assert here for type checking purposes:
        assert isinstance(value, typing.ForwardRef)

        message = f'Unable to evaluate type annotation {value.__forward_arg__!r}.'
        if sys.version_info >= (3, 11):
            e.add_note(message)
            raise
        else:
            raise TypeError(message) from e
    except RecursionError as e:
        # TODO ideally recursion errors should be checked in `eval_type` above, but `eval_type_backport`
        # is used directly in some places.
        message = (
            "If you made use of an implicit recursive type alias (e.g. `MyType = list['MyType']), "
            'consider using PEP 695 type aliases instead. For more details, refer to the documentation: '
            f'https://docs.pydantic.dev/{version_short()}/concepts/types/#named-recursive-types'
        )
        if sys.version_info >= (3, 11):
            e.add_note(message)
            raise
        else:
            raise RecursionError(f'{e.args[0]}\n{message}')

