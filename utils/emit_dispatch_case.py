
def emit_dispatch_case(
    overload: PythonSignatureGroup,
    structseq_typenames: dict[str, str],
    *,
    symint: bool = True,
) -> str:
    """
    Emit dispatch code for a single parsed signature. This corresponds to either
    a single native function, or a pair that differ only in output params. In the
    latter case, a single python signature is used for both and dispatching
    switches on the presence/absence of passed output args.
    """
    if overload.outplace is not None:
        # dispatch output and no-output variants, branch on _r.isNone(<out_idx>)
        return PY_VARIABLE_OUT.substitute(
            out_idx=overload.signature.output_idx(),
            call_dispatch=emit_single_dispatch(
                overload.signature, overload.base, structseq_typenames, symint=symint
            ),
            call_dispatch_out=emit_single_dispatch(
                overload.signature,
                overload.outplace,
                structseq_typenames,
                symint=symint,
            ),
        )
    else:
        # no-output version only
        return emit_single_dispatch(
            overload.signature, overload.base, structseq_typenames, symint=symint
        )

