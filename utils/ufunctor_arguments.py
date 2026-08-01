
def ufunctor_arguments(
    g: NativeFunctionsGroup, *, scalar_tensor_idx: int | None, scalar_t: BaseCppType
) -> UfunctorBindings:
    ctor = []
    apply = []
    for a in g.functional.func.arguments.flat_non_out:
        if a.type.is_tensor_like():
            if scalar_tensor_idx == 0:
                # put it in the ctor anyway
                ctor.append(ufunctor_ctor_argument(a, scalar_t=scalar_t))
                scalar_tensor_idx = None
            else:
                if scalar_tensor_idx is not None:
                    scalar_tensor_idx -= 1
                apply.append(ufunctor_apply_argument(a, scalar_t=scalar_t))
        else:
            ctor.append(ufunctor_ctor_argument(a, scalar_t=scalar_t))
    if scalar_tensor_idx is not None:
        raise AssertionError("scalar_tensor_idx should be None at end of processing")
    return UfunctorBindings(ctor=ctor, apply=apply)

