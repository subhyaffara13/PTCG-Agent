
def _sparsetensorcrdtransdirectionattr(x, context):
    return _ods_ir.Attribute.parse(f'#sparse_tensor<CrdTransDirection {str(x)}>', context=context)

