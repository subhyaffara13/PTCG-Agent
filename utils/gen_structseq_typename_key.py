
def gen_structseq_typename_key(f: NativeFunction) -> str:
    name = cpp.name(f.func)
    fieldnames = structseq_fieldnames(f.func.returns)
    return "_".join([name] + fieldnames)

