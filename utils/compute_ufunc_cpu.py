
def compute_ufunc_cpu(g: NativeFunctionsGroup) -> str:
    stub_sig = StubSignature(g)
    sig = StructuredImplSignature(g, ufunc.kernel_name(g, DispatchKey.CPU))

    return f"""
{stub_sig.type_defn()};
{stub_sig.dispatch_decl()}
{stub_sig.dispatch_defn()};

{sig.defn()} {{
  {stub_sig.call(sig.arguments())};
}}
"""

