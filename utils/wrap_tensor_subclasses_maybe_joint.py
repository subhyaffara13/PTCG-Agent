
def wrap_tensor_subclasses_maybe_joint(
    unwrapped_args: Sequence[Any],
    *,
    is_joint_structure: bool,
    meta: ViewAndMutationMeta,
) -> tuple[Any, ...]:
    # Since this function is reused for both inference and joint graphs,
    if is_joint_structure:
        if not (isinstance(unwrapped_args, tuple) and len(unwrapped_args) == 2):
            unwrapped_len = (
                len(unwrapped_args)
                if isinstance(unwrapped_args, (tuple, list))
                else "N/A"
            )
            raise AssertionError(
                f"expected tuple of length 2 for joint structure, "
                f"got {type(unwrapped_args)} with length {unwrapped_len}"
            )
        if not (
            isinstance(unwrapped_args[0], (tuple, list))
            and isinstance(unwrapped_args[1], (tuple, list))
        ):
            raise AssertionError(
                f"expected primals and tangents to be tuple or list, got {type(unwrapped_args[0])} and {type(unwrapped_args[1])}"
            )
        primals, tangents = unwrapped_args[0], unwrapped_args[1]
        wrapped_primals = wrap_tensor_subclasses(
            primals,
            subclass_metas=meta.subclass_inp_meta,
            included_subclass_symints=True,
        )
        wrapped_tangents = wrap_tensor_subclasses(
            tangents,
            subclass_metas=meta.subclass_tangent_meta,
            included_subclass_symints=False,
        )
        return (wrapped_primals, wrapped_tangents)
    else:
        wrapped_args = wrap_tensor_subclasses(
            unwrapped_args,
            subclass_metas=meta.subclass_inp_meta,
            included_subclass_symints=True,
        )
        return wrapped_args

