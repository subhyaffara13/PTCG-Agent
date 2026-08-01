
def _llvm_fastmathflagsattr(x, context):
    return _ods_ir.Attribute.parse(f'#llvm.fastmath<{str(x)}>', context=context)

