
def is_more_precise(left: Type, right: Type, *, ignore_promotions: bool = False) -> bool:
    """Check if left is a more precise type than right.

    A left is a proper subtype of right, left is also more precise than
    right. Also, if right is Any, left is more precise than right, for
    any left.
    """
    # TODO Should List[int] be more precise than List[Any]?
    right = get_proper_type(right)
    if isinstance(right, AnyType):
        return True
    return is_proper_subtype(left, right, ignore_promotions=ignore_promotions)


def is_more_precise(t1: object, t2: object) -> bool:
    """
    A binary relation denoted by <= that determines if t1 is more precise than t2.
    The relation is reflexive and transitive.
    returns True if t1 is more precise than t2 and False otherwise.
    Example:
        Dyn >= TensorType((1,2,3))
        int >= Dyn
        int >= int
        TensorType((1,Dyn,3)) <= TensorType((1,2,3))
    """
    if t1 == t2:
        return True

    if isinstance(t2, _DynType):
        return True

    if isinstance(t1, TensorType) and isinstance(t2, TensorType):
        return len(t1.__args__) == len(t2.__args__) and all(
            is_more_precise(elem1, elem2)
            for elem1, elem2 in zip(t1.__args__, t2.__args__)
        )

    else:
        return False

