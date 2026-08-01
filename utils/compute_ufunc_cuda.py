
def compute_ufunc_cuda(g: NativeFunctionsGroup) -> str:
    # First, build the functors, indexing them by dtype
    ufunctor_sigs, ufunctors = compute_ufunc_cuda_functors(g)

    # Next, build the conditionals
    sig = StructuredImplSignature(g, ufunc.kernel_name(g, DispatchKey.CUDA))
    dtype_cases = []
    for dtype, inner_ufunc_sigs in ufunctor_sigs.items():
        dtype_cases.append(
            f"""
AT_DISPATCH_CASE(at::ScalarType::{dtype},
  [&]() {{
    {compute_ufunc_cuda_dtype_body(g, dtype, inner_ufunc_sigs, sig.arguments())}
  }}
)
"""
        )

    dtype_cases_str = "\n".join(dtype_cases)

    stub_sig = StubSignature(g)

    return f"""
{ufunctors}

{stub_sig.type_defn()};
{stub_sig.dispatch_decl()}

{stub_sig.kernel_defn()} {{
  AT_DISPATCH_SWITCH(iter.common_dtype(), "{sig.name}",
    {dtype_cases_str}
  );
}}
REGISTER_DISPATCH({stub_sig.name}, &{stub_sig.kernel_name})

{sig.defn()} {{
  {stub_sig.direct_call(sig.arguments())};
}}
"""

