
def _remove_redundant_union_items(items: list[Type], keep_erased: bool) -> list[Type]:
    from mypy.subtypes import is_proper_subtype

    # The first pass through this loop, we check if later items are subtypes of earlier items.
    # The second pass through this loop, we check if earlier items are subtypes of later items
    # (by reversing the remaining items)
    for _direction in range(2):
        new_items: list[Type] = []
        # seen is a map from a type to its index in new_items
        seen: dict[ProperType, int] = {}
        unduplicated_literal_fallbacks: set[Instance] | None = None
        for ti in items:
            proper_ti = get_proper_type(ti)

            # UninhabitedType is always redundant
            if isinstance(proper_ti, UninhabitedType):
                continue

            duplicate_index = -1
            # Quickly check if we've seen this type
            if proper_ti in seen:
                duplicate_index = seen[proper_ti]
            elif (
                isinstance(proper_ti, LiteralType)
                and unduplicated_literal_fallbacks is not None
                and proper_ti.fallback in unduplicated_literal_fallbacks
            ):
                # This is an optimisation for unions with many LiteralType
                # We've already checked for exact duplicates. This means that any super type of
                # the LiteralType must be a super type of its fallback. If we've gone through
                # the expensive loop below and found no super type for a previous LiteralType
                # with the same fallback, we can skip doing that work again and just add the type
                # to new_items
                pass
            else:
                # If not, check if we've seen a supertype of this type
                for j, tj in enumerate(new_items):
                    proper_tj = get_proper_type(tj)
                    # If tj is an Instance with a last_known_value, do not remove proper_ti
                    # (unless it's an instance with the same last_known_value)
                    if (
                        isinstance(proper_tj, Instance)
                        and proper_tj.last_known_value is not None
                        and not (
                            isinstance(proper_ti, Instance)
                            and proper_tj.last_known_value == proper_ti.last_known_value
                        )
                    ):
                        continue

                    if is_proper_subtype(
                        ti, tj, keep_erased_types=keep_erased, ignore_promotions=True
                    ):
                        duplicate_index = j
                        break
            if duplicate_index != -1:
                # If deleted subtypes had more general truthiness, use that
                orig_item = new_items[duplicate_index]
                if not orig_item.can_be_true and ti.can_be_true:
                    new_items[duplicate_index] = true_or_false(orig_item)
                elif not orig_item.can_be_false and ti.can_be_false:
                    new_items[duplicate_index] = true_or_false(orig_item)
            else:
                # We have a non-duplicate item, add it to new_items
                seen[proper_ti] = len(new_items)
                new_items.append(ti)
                if isinstance(proper_ti, LiteralType):
                    if unduplicated_literal_fallbacks is None:
                        unduplicated_literal_fallbacks = set()
                    unduplicated_literal_fallbacks.add(proper_ti.fallback)

        items = new_items
        if len(items) <= 1:
            break
        items.reverse()

    return items

