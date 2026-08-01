
def _sparsetensorstoragespecifierkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#sparse_tensor<kind {str(x)}>', context=context)

