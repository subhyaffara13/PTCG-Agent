
def structseq_fieldnames(returns: tuple[Return, ...]) -> list[str]:
    if len(returns) <= 1 or all(r.name is None for r in returns):
        return []
    else:
        if any(r.name is None for r in returns):
            # When building on Windows, `PyStructSequence_UnnamedField` could not be
            # resolved by the linker for some reason, which cause error in building:
            #
            # python_nn_functions.cpp.obj : error LNK2001: unresolved external symbol
            # PyStructSequence_UnnamedField
            #
            # Thus, at this point in time, we do not support unnamed
            # fields in structseq; you must either name all fields,
            # or none of them.
            raise ValueError("Unnamed field is not supported by codegen")

        return [str(r.name) for r in returns]

