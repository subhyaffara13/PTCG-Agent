
def _check_alias_info(
    context: str,
    real_out: PyTree,
    real_in: PyTree,
    fake_out: PyTree,
    fake_in: PyTree,
) -> None:
    r_aliasing = outputs_alias_inputs(real_out, real_in)
    f_aliasing = outputs_alias_inputs(fake_out, fake_in)
    if r_aliasing != f_aliasing:
        raise MetadataMismatchError(
            f"{context} mismatch in outputs_alias_inputs check {f_aliasing} != {r_aliasing}"
        )

    r_identity_eq = outputs_are_inputs(real_out, real_in)
    f_identity_eq = outputs_are_inputs(fake_out, fake_in)
    if r_identity_eq != f_identity_eq:
        raise MetadataMismatchError(
            f"{context} mismatch in outputs_are_inputs check {f_identity_eq} != {r_identity_eq}"
        )

    r_output_alias_each_other = output_alias_each_other(real_out)
    f_output_alias_each_other = output_alias_each_other(fake_out)
    if r_output_alias_each_other != f_output_alias_each_other:
        raise MetadataMismatchError(
            f"{context} mismatch in outputs_alias_each_other check "
            f"{f_output_alias_each_other} != {r_output_alias_each_other}"
        )

