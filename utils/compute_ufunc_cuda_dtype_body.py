
def compute_ufunc_cuda_dtype_body(
    g: NativeFunctionsGroup,
    dtype: ScalarType,
    inner_loops: dict[UfuncKey, UfunctorSignature],
    parent_ctx: Sequence[Binding],
) -> str:
    body = "using opmath_t = at::opmath_type<scalar_t>;"
    body += "if (false) {}\n"  # for ease of codegen
    for config in BinaryScalarSpecializationConfigs:
        if config.ufunc_key not in inner_loops:
            continue
        ufunctor_sig = inner_loops[config.ufunc_key]
        scalar_idx = config.scalar_idx + 1
        # Make a copy and at the same time widen the type (not permissible
        # without copy; we don't want to mutate the input argument anyway)
        ctx: list[Expr | Binding] = list(parent_ctx)
        ctx.append(
            Expr(
                expr=f"iter.scalar_value<opmath_t>({scalar_idx})",
                type=NamedCType(config.ctor_tensor, BaseCType(opmath_t)),
            )
        )
        ufunctor_ctor_exprs_str = ", ".join(
            a.expr for a in translate(ctx, ufunctor_sig.arguments().ctor)
        )

        # NB: ufunctor must be allocated before iter.remove_operand is called,
        # as it relies on iter
        body += f"""\
else if (iter.is_cpu_scalar({scalar_idx})) {{
  {ufunctor_sig.name}<scalar_t> ufunctor({ufunctor_ctor_exprs_str});
  iter.remove_operand({scalar_idx});
  gpu_kernel(iter, ufunctor);
}}"""

    ufunctor_sig = inner_loops[UfuncKey.CUDAFunctor]
    ufunctor_ctor_exprs_str = ", ".join(
        a.expr for a in translate(parent_ctx, ufunctor_sig.arguments().ctor)
    )
    body += f"""
else {{
  gpu_kernel(iter, {ufunctor_sig.name}<scalar_t>({ufunctor_ctor_exprs_str}));
}}
    """
    return body

