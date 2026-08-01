
def iscomplexfunction_warn(rout):
    if iscomplexfunction(rout):
        outmess("""\
    **************************************************************
        Warning: code with a function returning complex value
        may not work correctly with your Fortran compiler.
        When using GNU gcc/g77 compilers, codes should work
        correctly for callbacks with:
        f2py -c -DF2PY_CB_RETURNCOMPLEX
    **************************************************************\n""")
        return 1
    return 0

