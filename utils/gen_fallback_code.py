
def gen_fallback_code(
    schema: LazyIrSchema,
    sig: DispatcherSignature | NativeSignature,
    overload_name: str,
) -> str:
    """
    Generate code that falls back to eager conditioned on a predicate
    """
    dispatcher_sig = DispatcherSignature.from_schema(schema.func)
    exprs = translate(sig.arguments(), dispatcher_sig.arguments())
    fallback_args = ",\n                ".join([a.expr for a in exprs])
    if len(overload_name):
        aten_op_str = f"ATEN_OP2({schema.aten_name}, {overload_name})"
    else:
        aten_op_str = f"ATEN_OP({schema.aten_name})"
    return f"""
        if (force_eager_fallback({aten_symbol(schema)})) {{
            return at::native::call_fallback_fn_symint<&ltc_eager_fallback, {aten_op_str}>::call(
                {fallback_args}
            );
        }}
"""

