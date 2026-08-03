import functools
import sys
from typing import Any, List

def replace_types(type_: Any, type_map: Mapping[Any, Any]) -> Any:
    """Return type with all occurrences of `type_map` keys recursively replaced with their values.

    :param type_: Any type, class or generic alias
    :param type_map: Mapping from `TypeVar` instance to concrete types.
    :return: New type representing the basic structure of `type_` with all
        `typevar_map` keys recursively replaced.

    >>> replace_types(Tuple[str, Union[List[str], float]], {str: int})
    Tuple[int, Union[List[int], float]]

    """
    if not type_map:
        return type_

    type_args = get_args(type_)
    origin_type = get_origin(type_)

    if origin_type is Annotated:
        annotated_type, *annotations = type_args
        return Annotated[replace_types(annotated_type, type_map), tuple(annotations)]

    if (origin_type is ExtLiteral) or (sys.version_info >= (3, 8) and origin_type is Literal):
        return type_map.get(type_, type_)
    # Having type args is a good indicator that this is a typing module
    # class instantiation or a generic alias of some sort.
    if type_args:
        resolved_type_args = tuple(replace_types(arg, type_map) for arg in type_args)
        if all_identical(type_args, resolved_type_args):
            # If all arguments are the same, there is no need to modify the
            # type or create a new object at all
            return type_
        if (
            origin_type is not None
            and isinstance(type_, typing_base)
            and not isinstance(origin_type, typing_base)
            and getattr(type_, '_name', None) is not None
        ):
            # In python < 3.9 generic aliases don't exist so any of these like `list`,
            # `type` or `collections.abc.Callable` need to be translated.
            # See: https://www.python.org/dev/peps/pep-0585
            origin_type = getattr(typing, type_._name)
        assert origin_type is not None
        # PEP-604 syntax (Ex.: list | str) is represented with a types.UnionType object that does not have __getitem__.
        # We also cannot use isinstance() since we have to compare types.
        if sys.version_info >= (3, 10) and origin_type is types.UnionType:  # noqa: E721
            return functools.reduce(operator.or_, resolved_type_args)
        return origin_type[resolved_type_args]

    # We handle pydantic generic models separately as they don't have the same
    # semantics as "typing" classes or generic aliases
    if not origin_type and lenient_issubclass(type_, GenericModel) and not type_.__concrete__:
        type_args = type_.__parameters__
        resolved_type_args = tuple(replace_types(t, type_map) for t in type_args)
        if all_identical(type_args, resolved_type_args):
            return type_
        return type_[resolved_type_args]

    # Handle special case for typehints that can have lists as arguments.
    # `typing.Callable[[int, str], int]` is an example for this.
    if isinstance(type_, (List, list)):
        resolved_list = list(replace_types(element, type_map) for element in type_)
        if all_identical(type_, resolved_list):
            return type_
        return resolved_list

    # For JsonWrapperValue, need to handle its inner type to allow correct parsing
    # of generic Json arguments like Json[T]
    if not origin_type and lenient_issubclass(type_, JsonWrapper):
        type_.inner_type = replace_types(type_.inner_type, type_map)
        return type_

    # If all else fails, we try to resolve the type directly and otherwise just
    # return the input with no modifications.
    new_type = type_map.get(type_, type_)
    # Convert string to ForwardRef
    if isinstance(new_type, str):
        return ForwardRef(new_type)
    else:
        return new_type


def replace_types(type_: Any, type_map: Mapping[TypeVar, Any] | None) -> Any:
    """Return type with all occurrences of `type_map` keys recursively replaced with their values.

    Args:
        type_: The class or generic alias.
        type_map: Mapping from `TypeVar` instance to concrete types.

    Returns:
        A new type representing the basic structure of `type_` with all
        `typevar_map` keys recursively replaced.

    Example:
        ```python
        from typing import Union

        from pydantic._internal._generics import replace_types

        replace_types(tuple[str, Union[list[str], float]], {str: int})
        #> tuple[int, Union[list[int], float]]
        ```
    """
    if not type_map:
        return type_

    type_args = get_args(type_)
    origin_type = get_origin(type_)

    if typing_objects.is_annotated(origin_type):
        annotated_type, *annotations = type_args
        annotated_type = replace_types(annotated_type, type_map)
        # TODO remove parentheses when we drop support for Python 3.10:
        return Annotated[(annotated_type, *annotations)]

    # Having type args is a good indicator that this is a typing special form
    # instance or a generic alias of some sort.
    if type_args:
        resolved_type_args = tuple(replace_types(arg, type_map) for arg in type_args)
        if all_identical(type_args, resolved_type_args):
            # If all arguments are the same, there is no need to modify the
            # type or create a new object at all
            return type_

        if (
            origin_type is not None
            and isinstance(type_, _typing_extra.typing_base)
            and not isinstance(origin_type, _typing_extra.typing_base)
            and getattr(type_, '_name', None) is not None
        ):
            # In python < 3.9 generic aliases don't exist so any of these like `list`,
            # `type` or `collections.abc.Callable` need to be translated.
            # See: https://www.python.org/dev/peps/pep-0585
            origin_type = getattr(typing, type_._name)
        assert origin_type is not None

        if is_union_origin(origin_type):
            if any(typing_objects.is_any(arg) for arg in resolved_type_args):
                # `Any | T` ~ `Any`:
                resolved_type_args = (Any,)
            # `Never | T` ~ `T`:
            resolved_type_args = tuple(
                arg
                for arg in resolved_type_args
                if not (typing_objects.is_noreturn(arg) or typing_objects.is_never(arg))
            )

        # PEP-604 syntax (e.g. `list | str`) is represented with a types.UnionType object that does not
        # implement `__getitem__()`. In Python 3.14+, `typing.Union` and `types.UnionType` are the same,
        # and we instead rely on `typing.Union` as it implicitly converts string annotations to `ForwardRef`
        # instances (this is to avoid type errors as per https://github.com/python/cpython/pull/105366).
        # TODO remove type ignore comment when we drop support for Python 3.9 (https://github.com/microsoft/pyright/issues/11241):
        if (3, 10) <= sys.version_info < (3, 14) and origin_type is types.UnionType:  # pyright: ignore[reportAttributeAccessIssue]
            return reduce(operator.or_, resolved_type_args)
        # NotRequired[T] and Required[T] don't support tuple type resolved_type_args, hence the condition below
        return origin_type[resolved_type_args[0] if len(resolved_type_args) == 1 else resolved_type_args]

    # We handle pydantic generic models separately as they don't have the same
    # semantics as "typing" classes or generic aliases

    if not origin_type and is_model_class(type_):
        parameters = type_.__pydantic_generic_metadata__['parameters']
        if not parameters:
            return type_
        resolved_type_args = tuple(replace_types(t, type_map) for t in parameters)
        if all_identical(parameters, resolved_type_args):
            return type_
        return type_[resolved_type_args]

    # Handle special case for typehints that can have lists as arguments.
    # `typing.Callable[[int, str], int]` is an example for this.
    if isinstance(type_, list):
        resolved_list = [replace_types(element, type_map) for element in type_]
        if all_identical(type_, resolved_list):
            return type_
        return resolved_list

    # If all else fails, we try to resolve the type directly and otherwise just
    # return the input with no modifications.
    return type_map.get(type_, type_)

