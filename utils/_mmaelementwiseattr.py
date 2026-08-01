
def _mmaelementwiseattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<mma_element_wise {str(x)}>', context=context)

