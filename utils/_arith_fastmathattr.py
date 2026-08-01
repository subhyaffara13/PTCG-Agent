
def _arith_fastmathattr(x, context):
    return _ods_ir.Attribute.parse(f'#arith.fastmath<{str(x)}>', context=context)

