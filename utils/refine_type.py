
def refine_type(ti: Type, si: Type) -> Type:
    """Refine `ti` by replacing Anys in it with information taken from `si`

    This basically works by, when the types have the same structure,
    traversing both of them in parallel and replacing Any on the left
    with whatever the type on the right is. If the types don't have the
    same structure (or aren't supported), the left type is chosen.

    For example:
      refine(Any, T) = T,  for all T
      refine(float, int) = float
      refine(List[Any], List[int]) = List[int]
      refine(Dict[int, Any], Dict[Any, int]) = Dict[int, int]
      refine(Tuple[int, Any], Tuple[Any, int]) = Tuple[int, int]

      refine(Callable[[Any], Any], Callable[[int], int]) = Callable[[int], int]
      refine(Callable[..., int], Callable[[int, float], Any]) = Callable[[int, float], int]

      refine(Optional[Any], int) = Optional[int]
      refine(Optional[Any], Optional[int]) = Optional[int]
      refine(Optional[Any], Union[int, str]) = Optional[Union[int, str]]
      refine(Optional[List[Any]], List[int]) = List[int]

    """
    t = get_proper_type(ti)
    s = get_proper_type(si)

    if isinstance(t, AnyType):
        # If s is also an Any, we return if it is a missing_import Any
        return t if isinstance(s, AnyType) and t.missing_import_name else s

    if isinstance(t, Instance) and isinstance(s, Instance) and t.type == s.type:
        return t.copy_modified(args=[refine_type(ta, sa) for ta, sa in zip(t.args, s.args)])

    if (
        isinstance(t, TupleType)
        and isinstance(s, TupleType)
        and t.partial_fallback == s.partial_fallback
        and len(t.items) == len(s.items)
    ):
        return t.copy_modified(items=[refine_type(ta, sa) for ta, sa in zip(t.items, s.items)])

    if isinstance(t, CallableType) and isinstance(s, CallableType):
        return refine_callable(t, s)

    if isinstance(t, UnionType):
        return refine_union(t, s)

    # TODO: Refining of builtins.tuple, Type?

    return t

