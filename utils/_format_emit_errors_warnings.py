
def _format_emit_errors_warnings(err_lst):
    """Format/emit errors/warnings from a lowlevel batched routine.

    See inv, solve.
    """
    singular, lapack_err, ill_cond = [], [], []
    for i, dct in enumerate(err_lst):
        if dct["is_singular"]:
            singular.append(i)
        if dct["lapack_info"] < 0:
            lapack_err.append(f"slice {i} emits lapack info={dct['lapack_info']}")
        if dct["is_ill_conditioned"]:
            ill_cond.append(f"slice {i} has rcond = {dct['rcond']}")

    if singular:
        raise LinAlgError(
            f"A singular matrix detected: slice(s) {singular} are singular."
        )

    if lapack_err:
        raise ValueError(f"Internal LAPACK errors: {','.join(lapack_err)}.")

    if ill_cond:
       warnings.warn(
            f"An ill-conditioned matrix detected: {','.join(ill_cond)}.",
            LinAlgWarning,
            stacklevel=3
        )


def _format_emit_errors_warnings(err_lst, lapack_driver):
    """Format/emit errors/warnings from a lowlevel batched routine.
    """
    # NB the low-level routine currently stops processing a batch at the first error
    for entry in err_lst:
        info = entry["lapack_info"]
        num = entry["num"]
        if info != 0:
            if info > 0:
                raise LinAlgError(f"SVD did not converge for slice = {num}.")
            if info < 0:
                if lapack_driver == "gesdd" and info == -4:
                    msg = f"slice {num} has a NaN entry"
                    raise ValueError(msg)
                raise ValueError(
                    f'illegal value in {-info}th argument of internal {lapack_driver}'
                    f'  for slice {num}.'
                )

