
def make_simplified_union(
    items: Sequence[Type],
    line: int = -1,
    column: int = -1,
    *,
    keep_erased: bool = False,
    contract_literals: bool = True,
    handle_recursive: bool = True,
) -> ProperType:
    """Build union type with redundant union items removed.

    If only a single item remains, this may return a non-union type.

    Examples:

    * [int, str] -> Union[int, str]
    * [int, object] -> object
    * [int, int] -> int
    * [int, Any] -> Union[int, Any] (Any types are not simplified away!)
    * [Any, Any] -> Any
    * [int, Union[bytes, str]] -> Union[int, bytes, str]

    Note: This must NOT be used during semantic analysis, since TypeInfos may not
          be fully initialized.

    The keep_erased flag is used for type inference against union types
    containing type variables. If set to True, keep all ErasedType items.

    The contract_literals flag indicates whether we need to contract literal types
    back into a sum type. Set it to False when called by try_expanding_sum_type_
    to_union().
    """
    # Step 1: expand all nested unions
    items = flatten_nested_unions(items, handle_recursive=handle_recursive)

    # Step 2: fast path for single item
    if len(items) == 1:
        return get_proper_type(items[0])

    # Step 3: remove redundant unions
    simplified_set: Sequence[Type] = _remove_redundant_union_items(items, keep_erased)

    # Step 4: If more than one literal exists in the union, try to simplify
    if (
        contract_literals
        and sum(isinstance(get_proper_type(item), LiteralType) for item in simplified_set) > 1
    ):
        simplified_set = try_contracting_literals_in_union(simplified_set)

    result = get_proper_type(UnionType.make_union(simplified_set, line, column))

    nitems = len(items)
    if nitems > 1 and (
        nitems > 2 or not (type(items[0]) is NoneType or type(items[1]) is NoneType)
    ):
        # Step 5: At last, we erase any (inconsistent) extra attributes on instances.

        # Initialize with None instead of an empty set as a micro-optimization. The set
        # is needed very rarely, so we try to avoid constructing it.
        extra_attrs_set: set[ExtraAttrs] | None = None
        for item in items:
            instance = try_getting_instance_fallback(item)
            if instance and instance.extra_attrs:
                if extra_attrs_set is None:
                    extra_attrs_set = {instance.extra_attrs}
                else:
                    extra_attrs_set.add(instance.extra_attrs)

        # Code below is awkward, because we don't want the extra checks to affect
        # performance in the common case.
        erase_extra = False
        if extra_attrs_set is not None:
            fallback = try_getting_instance_fallback(result)
            if fallback is None:
                return result
            if len(extra_attrs_set) > 1:  # This case is too tricky to handle.
                erase_extra = True
            else:
                # Check that all relevant items have the extra attributes.
                for item in items:
                    instance = try_getting_instance_fallback(item)
                    if instance and instance.type == fallback.type and not instance.extra_attrs:
                        erase_extra = True
                        break
            if erase_extra:
                fallback.extra_attrs = None

    return result

