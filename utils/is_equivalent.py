from typing import Callable

def is_equivalent(
    a: Type,
    b: Type,
    *,
    ignore_type_params: bool = False,
    ignore_pos_arg_names: bool = False,
    options: Options | None = None,
    subtype_context: SubtypeContext | None = None,
) -> bool:
    return is_subtype(
        a,
        b,
        ignore_type_params=ignore_type_params,
        ignore_pos_arg_names=ignore_pos_arg_names,
        options=options,
        subtype_context=subtype_context,
    ) and is_subtype(
        b,
        a,
        ignore_type_params=ignore_type_params,
        ignore_pos_arg_names=ignore_pos_arg_names,
        options=options,
        subtype_context=subtype_context,
    )


def is_equivalent(
    spec1: TreeSpec,
    spec2: TreeSpec,
    equivalence_fn: Callable[[type | None, Context, type | None, Context], bool],
) -> bool:
    """Customizable equivalence check for two TreeSpecs.

    Arguments:
        spec1: The first TreeSpec to compare
        spec2: The second TreeSpec to compare
        equivalence_fn: A function to determine the equivalence of two
            TreeSpecs by examining their types and contexts. It will be called like:

                equivalence_fn(spec1.type, spec1.context, spec2.type, spec2.context)

            This function will be applied recursively to all children.

    Returns:
        True if the two TreeSpecs are equivalent, False otherwise.
    """
    if not equivalence_fn(spec1.type, spec1.context, spec2.type, spec2.context):
        return False

    # Recurse on children
    if spec1.num_children != spec2.num_children:
        return False

    for child_spec1, child_spec2 in zip(spec1.children(), spec2.children()):
        if not is_equivalent(child_spec1, child_spec2, equivalence_fn):
            return False

    return True

