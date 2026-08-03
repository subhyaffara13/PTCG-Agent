from typing import Any, Callable

def all_gather_object_enforce_type(
    pg: dist.ProcessGroup,
    # pyre-fixme[2]: Parameter must have a type that does not contain `Any`
    object_list: list[Any],
    # pyre-fixme[2]: Parameter must have a type other than `Any`
    obj: Any,
    # pyre-fixme[2]: Parameter must have a type that does not contain `Any`
    type_checker: Callable[[Any, Any], bool] = lambda x, y: type(x) is type(y),
) -> None:
    """
    Similar to plain all_gather_object but with additional type checking
    AFTER gather is done to ensure basic consistency.
    If check does not pass, all ranks will fail with exception.

    This is generally to prevent conditional logic leading to
    unexpected messages being received. This is considered fatal code error,
    but due to logic stacks this might happen implicitly in practice.

    The default check does not check sub type (considered different)
    or covariance (considered same) but users can pass in custom checker
    if more complicated check is needed.
    """
    dist.all_gather_object(object_list, obj, group=pg)

    # conservative check
    list_len = len(object_list)
    if list_len == 0:
        return
    first_obj = object_list[0]
    for i in range(1, list_len):
        if not type_checker(first_obj, object_list[i]):
            raise TypeError(
                f"Object type at index {i} is {type(object_list[i])}, "
                f"while first object type is {type(first_obj)}"
            )

