from typing import Callable

def are_args_compatible(
    left: FormalArgument,
    right: FormalArgument,
    is_compat: Callable[[Type, Type], bool],
    *,
    ignore_pos_arg_names: bool,
    allow_partial_overlap: bool,
    allow_imprecise_kinds: bool = False,
) -> bool:
    if left.required and right.required:
        # If both arguments are required allow_partial_overlap has no effect.
        allow_partial_overlap = False

    def is_different(
        left_item: object | None, right_item: object | None, allow_overlap: bool
    ) -> bool:
        """Checks if the left and right items are different.

        If the right item is unspecified (e.g. if the right callable doesn't care
        about what name or position its arg has), we default to returning False.

        If we're allowing partial overlap, we also default to returning False
        if the left callable also doesn't care."""
        if right_item is None:
            return False
        if allow_overlap and left_item is None:
            return False
        return left_item != right_item

    # If right has a specific name it wants this argument to be, left must
    # have the same.
    if is_different(left.name, right.name, allow_partial_overlap):
        # But pay attention to whether we're ignoring positional arg names
        if not ignore_pos_arg_names or right.pos is None:
            return False

    # If right is at a specific position, left must have the same.
    # TODO: partial overlap logic is flawed for positions.
    # We disable it to avoid false positives at a cost of few false negatives.
    if is_different(left.pos, right.pos, allow_overlap=False) and not allow_imprecise_kinds:
        return False

    # If right's argument is optional, left's must also be
    # (unless we're relaxing the checks to allow potential
    # rather than definite compatibility).
    if not allow_partial_overlap and not right.required and left.required:
        return False

    # If we're allowing partial overlaps and neither arg is required,
    # the types don't actually need to be the same
    if allow_partial_overlap and not left.required and not right.required:
        return True

    # Left must have a more general type
    return is_compat(right.typ, left.typ)

