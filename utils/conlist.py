
def conlist(
    item_type: type[AnyItemType],
    *,
    min_length: int | None = None,
    max_length: int | None = None,
    unique_items: bool | None = None,
) -> type[list[AnyItemType]]:
    """A wrapper around [`list`][] that adds validation.

    Args:
        item_type: The type of the items in the list.
        min_length: The minimum length of the list. Defaults to None.
        max_length: The maximum length of the list. Defaults to None.
        unique_items: Whether the items in the list must be unique. Defaults to None.
            !!! warning Deprecated
                The `unique_items` parameter is deprecated, use `Set` instead.
                See [this issue](https://github.com/pydantic/pydantic-core/issues/296) for more details.

    Returns:
        The wrapped list type.
    """
    if unique_items is not None:
        raise PydanticUserError(
            (
                '`unique_items` is removed, use `Set` instead'
                '(this feature is discussed in https://github.com/pydantic/pydantic-core/issues/296)'
            ),
            code='removed-kwargs',
        )
    return Annotated[list[item_type], annotated_types.Len(min_length or 0, max_length)]  # pyright: ignore[reportReturnType]


def conlist(
    item_type: Type[T], *, min_items: Optional[int] = None, max_items: Optional[int] = None, unique_items: bool = None
) -> Type[List[T]]:
    # __args__ is needed to conform to typing generics api
    namespace = dict(
        min_items=min_items, max_items=max_items, unique_items=unique_items, item_type=item_type, __args__=(item_type,)
    )
    # We use new_class to be able to deal with Generic types
    return new_class('ConstrainedListValue', (ConstrainedList,), {}, lambda ns: ns.update(namespace))

