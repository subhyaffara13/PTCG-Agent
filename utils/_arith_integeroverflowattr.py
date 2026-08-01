
def _arith_integeroverflowattr(x, context):
    return _ods_ir.Attribute.parse(f'#arith.overflow<{str(x)}>', context=context)

