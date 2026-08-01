
def is_overlapping_types_for_overload(left: Type, right: Type) -> bool:
    # Note that among other effects 'overlap_for_overloads' flag will effectively
    # ignore possible overlap between type variables and None. This is technically
    # unsafe, but unsafety is tiny and this prevents some common use cases like:
    #     @overload
    #     def foo(x: None) -> None: ..
    #     @overload
    #     def foo(x: T) -> Foo[T]: ...
    return is_overlapping_types(left, right, ignore_promotions=True, overlap_for_overloads=True)

