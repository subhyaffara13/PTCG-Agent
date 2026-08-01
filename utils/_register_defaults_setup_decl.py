
def _register_defaults_setup_decl(ir: ClassIR, module_name: str) -> None:
    sig = FuncSignature([RuntimeArg(SELF_NAME, RInstance(ir))], bool_rprimitive)
    ir.method_decls[MYPYC_DEFAULTS_SETUP] = FuncDecl(
        MYPYC_DEFAULTS_SETUP, ir.name, module_name, sig
    )

