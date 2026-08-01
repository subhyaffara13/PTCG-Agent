
def _llvm_integeroverflowflagsattr(x, context):
    return _ods_ir.Attribute.parse(f'#llvm.overflow<{str(x)}>', context=context)

