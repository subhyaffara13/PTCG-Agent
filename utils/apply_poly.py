
def apply_poly(tp: CallableType, poly_tvars: Sequence[TypeVarLikeType]) -> CallableType | None:
    """Make free type variables generic in the type if possible.

    This will translate the type `tp` while trying to create valid bindings for
    type variables `poly_tvars` while traversing the type. This follows the same rules
    as we do during semantic analysis phase, examples:
      * Callable[Callable[[T], T], T] -> def [T] (def (T) -> T) -> T
      * Callable[[], Callable[[T], T]] -> def () -> def [T] (T -> T)
      * List[T] -> None (not possible)
    """
    try:
        return tp.copy_modified(
            arg_types=[t.accept(PolyTranslator(poly_tvars)) for t in tp.arg_types],
            ret_type=tp.ret_type.accept(PolyTranslator(poly_tvars)),
            variables=[],
        )
    except PolyTranslationError:
        return None

